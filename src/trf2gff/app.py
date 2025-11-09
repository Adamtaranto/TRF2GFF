#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Converts Tandem Repeat Finder .dat file output into GFF3 format.
"""

# ████████╗██████╗ ███████╗██████╗  ██████╗ ███████╗███████╗
# ╚══██╔══╝██╔══██╗██╔════╝╚════██╗██╔════╝ ██╔════╝██╔════╝
#    ██║   ██████╔╝█████╗   █████╔╝██║  ███╗█████╗  █████╗
#    ██║   ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝
#    ██║   ██║  ██║██║     ███████╗╚██████╔╝██║     ██║
#    ╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚═╝

# Copyright (C) 2017-present Adam Taranto <adam.p.taranto@gmail.com>
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

import argparse
import csv
import logging
import os.path as op
import sys

from trf2gff._version import __version__


def mainArgs():
    """
    Parse command-line arguments for TRF to GFF3 conversion.

    Configures argument parser for input/output file paths, version display,
    and logging level settings. Automatically generates output filename from
    input filename if not specified and stdin is not being used.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments containing:

        - infile : str or None
            Path to input TRF .dat file
        - outgff : str
            Path to output GFF3 file or '-' for stdout
        - loglevel : str
            Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    See Also
    --------
    main : Main conversion function that uses these arguments.

    Notes
    -----
    If no output file is specified:

    - When reading from stdin: defaults to stdout ('-')
    - When reading from file: generates filename as <input_base>.gff3

    Examples
    --------
    Parse arguments for file input with auto-generated output name:

    >>> import sys
    >>> sys.argv = ['trf2gff', '-i', 'genome.dat']
    >>> args = mainArgs()
    >>> args.outgff
    'genome.gff3'

    Parse arguments for stdout output:

    >>> sys.argv = ['trf2gff', '-i', 'genome.dat', '-o', '-']
    >>> args = mainArgs()
    >>> args.outgff
    '-'
    """
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
        "-i",
        "--infile",
        type=str,
        default=None,
        required=False,
        help="dat file output from TRF.",
    )
    parser.add_argument(
        "-o",
        "--outgff",
        type=str,
        default=None,
        help="Name of gff output file. Set to '-' to write to stdout.",
    )
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level.",
    )
    args = parser.parse_args()

    # Set outfile with basename of datfile if outfile name not provided and not data on stdin.
    if not args.outgff and sys.stdin.isatty() and args.infile:
        args.outgff = op.splitext(args.infile)[0] + ".gff3"
    elif not args.outgff:
        args.outgff = "-"

    return args


def main():
    """
    Convert Tandem Repeat Finder .dat output to GFF3 format.

    Main entry point for the trf2gff command-line tool. Reads TRF .dat file
    data from either stdin or a specified file, parses tandem repeat features,
    and outputs them in GFF3 format to stdout or a specified file.

    The function performs the following workflow:

    1. Parse command-line arguments
    2. Configure logging
    3. Read input data (stdin or file)
    4. Parse TRF dat format lines
    5. Convert features to GFF3 format
    6. Write output (stdout or file)

    TRF .dat files contain sequence headers ("Sequence: <name>") followed by
    data lines with 15 space-separated fields per tandem repeat feature.

    GFF3 output includes columns for seqid, source (TRF), type (TRF_SSR),
    start, end, score (.), strand (.), phase (.), and attributes with
    key=value pairs containing TRF metadata.

    Raises
    ------
    SystemExit
        If input file doesn't exist or no input data is provided.
    ValueError
        If an invalid log level is specified.

    See Also
    --------
    mainArgs : Parse command-line arguments.

    Notes
    -----
    Input priority order:

    1. stdin (highest priority)
    2. --infile argument
    3. Error if neither available

    When reading from stdin, any --infile argument is ignored.

    Examples
    --------
    Convert file to stdout:

    >>> # Command line usage:
    >>> # trf2gff -i genome.fa.2.7.7.80.10.50.500.dat -o -

    Convert file with auto-generated output name:

    >>> # trf2gff -i genome.fa.2.7.7.80.10.50.500.dat

    Process stdin input:

    >>> # cat input.dat | trf2gff -o output.gff3
    """
    # Fetch args
    args = mainArgs()

    # Set up logging
    numeric_level = getattr(logging, args.loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % args.loglevel)

    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s", level=numeric_level
    )

    if not sys.stdin.isatty():
        # If data on stdin, set input_data to read from stdin
        logging.info("Reading input from stdin.")
        input_data = sys.stdin.readlines()
        if args.infile:
            # If infile is also set log that it will be ignored
            logging.warning(
                f"Ignoring --infile arg {args.infile} and reading data from stdin."
            )
    elif args.infile:
        # If infile is set, check if it exists
        if not op.exists(args.infile):
            logging.error(f"dat file not found: {args.infile}")
            sys.exit(1)
        else:
            # If file exists, readlines from file
            logging.info(f"Reading datfile: {args.infile}")
            with open(args.infile, "r") as fh:
                input_data = fh.readlines()
    else:
        # Exit if no data on stdin or infile
        logging.error("No input data detected. Exiting.")
        sys.exit(1)

    # Init feature counter
    counter = 0

    # Init seq name and counter
    seq_name = None
    seq_count = 0

    # Init gff line list
    outlines = list()

    # Preprocess incomming data to remove blank lines
    lines = [line for line in (ln.rstrip() for ln in input_data) if line]

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
                + repeat_seq,
            ]
            outlines.append(gff_line)

    logging.info(f"Converted {counter} features from {seq_count} sequences.")

    # If outfile set write gfflines to file.
    if args.outgff != "-":
        logging.info(f"Writing gff to file: {args.outgff}")
        with open(args.outgff, "w") as f:
            # Create csv writer with tab delimiters.
            csv_writer = csv.writer(f, delimiter="\t")
            # Convert list items to csv lines and write.
            csv_writer.writerows(outlines)
    else:
        logging.info("Writing gff to stdout")
        # Create csv writer with tab delimiters.
        csv_writer = csv.writer(sys.stdout, delimiter="\t")
        # Convert list items to csv lines and write.
        csv_writer.writerows(outlines)

    logging.info("Done!")


if __name__ == "__main__":
    main()
