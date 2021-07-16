# TRF2GFF
Convert Tandem Repeat Finder dat file output into gff3 format

Usage:

Example trf run:
```bash
trf genome.fasta 2 6 6 80 10 50 2000 -h
# Where args are Match, Mismatch, Delta, PM, PI, Minscore, MaxPeriod, [options]
```

Run TRF2GFF on trf dat file:
```bash
./TRF2GFF.py -d trf_output.dat -o reformated.gff3
```
