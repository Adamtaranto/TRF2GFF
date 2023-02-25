# TRF2GFF

Convert Tandem Repeat Finder dat file output into gff3 format.


## Installation

Install directly from this git repository.

```bash
pip install git+https://github.com/Adamtaranto/TRF2GFF.git
```

Or clone and install locally.

```bash
git clone https://github.com/Adamtaranto/TRF2GFF.git && cd TRF2GFF
pip install -e .
```

## Useage

Run trf:

```bash
trf genome.fa 2 6 6 80 10 50 2000 -h
# Where args are Match, Mismatch, Delta, PM, PI, Minscore, MaxPeriod, [options]
# Output: genome.fa.2.6.6.80.10.50.2000.dat
```


Convert dat file to gff3:

```bash
trf2gff -i trf_output.dat
# Output: genome.fa.2.6.6.80.10.50.2000.gff3
```
