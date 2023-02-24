# TRF2GFF

Convert Tandem Repeat Finder dat file output into gff3 format.


## Installing 

Install directly from this git repository.

```bash
pip install git+https://github.com/Adamtaranto/TRF2GFF.git
```

Or clone and install locally.

```bash
git clone https://github.com/Adamtaranto/TRF2GFF.git
cd TRF2GFF
pip install -e .
```

## Example useage

Example trf run:

```bash
trf genome.fasta 2 6 6 80 10 50 2000 -h
# Where args are Match, Mismatch, Delta, PM, PI, Minscore, MaxPeriod, [options]
```

Run TRF2GFF on trf dat file:

```bash
trf2gff -d trf_output.dat -o reformated.gff3
```
