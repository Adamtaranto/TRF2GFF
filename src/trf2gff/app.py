#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

████████╗██████╗ ███████╗██████╗  ██████╗ ███████╗███████╗
╚══██╔══╝██╔══██╗██╔════╝╚════██╗██╔════╝ ██╔════╝██╔════╝
   ██║   ██████╔╝█████╗   █████╔╝██║  ███╗█████╗  █████╗  
   ██║   ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝  
   ██║   ██║  ██║██║     ███████╗╚██████╔╝██║     ██║     
   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚═╝     

Converts Tandem Repeat Finder .dat file output into GFF3 format                                                          

"""

# Copyright (C) 2017-2023 Adam Taranto <adam.p.taranto@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from trf2gff import __version__
import argparse
import logging
import os.path as op
import sys


def mainArgs():
    parser = argparse.ArgumentParser(
        description="Converts Tandem Repeat Finder .dat file output into GFF3 format",
        prog="trf2gff",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    parser.add_argument(
        "-i", "--infile", type=str, required=True, help="dat file output from TRF."
    )
    parser.add_argument(
        "-o", "--outgff", type=str, default=None, help="Name of gff output file."
    )
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level.",
    )
    args = parser.parse_args()

    # Set outfile with basename of datfile if outfile name not provided
    if not args.outgff:
        args.outgff = op.splitext(args.infile)[0] + ".gff3"

    return args


def main():
    # Fetch args
    args = mainArgs()

    # Set up logging
    numeric_level = getattr(logging, args.loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.loglevel)

    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", level=numeric_level
    )

    if not op.exists(args.infile):
        logging.error(f"dat file not found: {args.infile}")
        sys.exit(1)

    logging.info(f"Reading datfile: {args.infile}")
    with open(args.infile) as fh:
        # Unpack lines from file
        lines = list(line for line in (ln.rstrip() for ln in fh) if line)

    # Init feature counter
    counter = 0

    # Init seq name and counter
    seq_name = None
    seq_count = 0

    # Init gff line list
    outlines = list()

    for line in lines:
        # Split line in space delimited elements
        ele = line.strip().split(" ")
        # Check if begining of new sequence and update current name
        if line.startswith("Sequence:"):
            seq_name = str(ele[1])
            seq_count += 1
            logging.info(f"Sequence found: {seq_name}")
        # Else check if data line and unpack fields
        elif ele[0][0].isdigit():
            counter += 1
            # Dat file fields
            # rep_start, rep_end, period_size, copy_no, pattern_size,
            # percent_match, percent_indel, align_score, a_percent,
            # c_percent, g_percent, t_percent, entropy, consensus, repeat
            [
                start,
                stop,
                period,
                copies,
                consensus_size,
                perc_match,
                perc_indels,
                align_score,
                perc_A,
                perc_C,
                perc_G,
                perc_T,
                entropy,
                cons_seq,
                repeat_seq,
            ] = ele

            # Convert to gff line
            gff_line = [
                seq_name,
                "TRF",
                "TRF_SSR",
                start,
                stop,
                ".",
                ".",
                ".",
                "ID=TRF_"
                + "{0:0>5}".format(counter)
                + ";period="
                + period
                + ";copies="
                + copies
                + ";consensus_size="
                + consensus_size
                + ";perc_match="
                + perc_match
                + ";perc_indels="
                + perc_indels
                + ";align_score="
                + align_score
                + ";entropy="
                + entropy
                + ";cons_seq="
                + cons_seq
                + ";repeat_seq="
                + repeat_seq
                + "\n",
            ]
            outlines.append(gff_line)

    logging.info(f"Converted {counter} features from {seq_count} sequences.")

    logging.info(f"Writing gff to file: {args.outgff}")
    f = open(args.outgff, "w")
    for gffline in outlines:
        f.write("\t".join(gffline))
    f.close()

    logging.info("Done!")


if __name__ == "__main__":
    main()
