#!/usr/bin/env python
#TRF2GFF.py
# Copyright (C) 2017 Adam Taranto <adam.taranto@anu.edu.au>
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

"""
Converts Tandem Repeat Finder .dat file output into GFF3 format
"""
#Example trf run:
#trf genome.fasta 2 6 6 80 10 50 2000 -h 
#Where arguements are Match, Mismatch, Delta, PM, PI, Minscore, MaxPeriod, [options]

#Usage:
#./TRF2GFF.py -d trf_output.dat -o reformated.gff3

import argparse
import os

def mainArgs():
	parser = argparse.ArgumentParser(
		description='Converts Tandem Repeat Finder .dat file output into GFF3 format',
		prog='TRF2GFF')
	parser.add_argument('-d',
						'--datfile',
						type=str,
						required=True,
						help='dat file output from TRF.')
	parser.add_argument('-o',
						'--outgff',
						type=str,
						default=None,
						help='Name of gff output file.')
	args = parser.parse_args()
	if not args.outgff:
		args.outgff = os.path.splitext(args.datfile)[0] + ".gff3"
		print(args.outgff)
	return args


def main():
	args = mainArgs()
	fname = args.datfile
	f = open(args.outgff, 'w')

	with open(fname) as fh:
		counter = int(1)
		lines = list(line for line in (l.rstrip() for l in fh) if line)
		for line in lines:
			ele = line.strip().split(" ")
			if line.startswith('Sequence:'):
				seq_name = ele[1]
			elif ele[0][0].isdigit():
				[start, stop, period, copies, 
				 consensus_size, perc_match, perc_indels, 
				 align_score, perc_A, perc_C, perc_G, perc_T, 
				 entropy, cons_seq, repeat_seq] = ele
				gff_line = [seq_name, 'TRF', 'TRF_SSR',
							start, stop, '.', '.', '.', 
							'ID=TRF_'+ '{0:0>5}'.format(counter) + 
							';period=' + period +
							';copies=' + copies +
							';consensus_size=' + consensus_size +
							';perc_match=' + perc_match +
							';perc_indels=' + perc_indels +
							';align_score=' + align_score +
							';entropy=' + entropy +
							';cons_seq=' + cons_seq +
							';repeat_seq=' + repeat_seq + '\n']
				counter += 1
				f.write('\t'.join(gff_line))
	f.close()

##Dat file fields
#rep_start, rep_end, period_size, copy_no, pattern_size, percent_match, percent_indel, align_score, a_percent, c_percent, g_percent, t_percent, entropy, consensus, repeat

if __name__== '__main__':
	main()