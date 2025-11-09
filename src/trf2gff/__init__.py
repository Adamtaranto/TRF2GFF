"""
TRF2GFF: Tandem Repeat Finder to GFF3 Converter.

A command-line tool for converting Tandem Repeat Finder (TRF) .dat file
output into standardized GFF3 format for downstream genomic analysis.

This package enables integration of tandem repeat annotations with genome
browsers and bioinformatics tools that use the GFF3 standard.

The main application module (app) contains CLI and conversion logic.

Notes
-----
For more information on Tandem Repeat Finder, see:
https://tandem.bu.edu/trf/trf.html

For GFF3 format specification, see:
https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md

Examples
--------
Command-line usage:

Convert TRF output to GFF3 file:

    $ trf2gff -i genome.fa.2.7.7.80.10.50.500.dat -o repeats.gff3

Process stdin and write to stdout:

    $ cat input.dat | trf2gff -o -
"""

from trf2gff._version import __version__

__all__ = ["__version__"]
