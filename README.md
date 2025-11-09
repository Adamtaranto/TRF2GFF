# TRF2GFF

```text
████████╗██████╗ ███████╗██████╗  ██████╗ ███████╗███████╗
╚══██╔══╝██╔══██╗██╔════╝╚════██╗██╔════╝ ██╔════╝██╔════╝
   ██║   ██████╔╝█████╗   █████╔╝██║  ███╗█████╗  █████╗
   ██║   ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══╝  ██╔══╝
   ██║   ██║  ██║██║     ███████╗╚██████╔╝██║     ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚═╝
```

Converts Tandem Repeat Finder .dat file output into GFF3 format.

## Installation

TRF2GFF requires Python >= v3.8

Install directly from this git repository.

```bash
pip install git+https://github.com/Adamtaranto/TRF2GFF.git
```

Or clone and install locally.

```bash
git clone https://github.com/Adamtaranto/TRF2GFF.git && cd TRF2GFF
pip install -e .
```

## Usage

### Run trf

```bash
trf genome.fa 2 6 6 80 10 50 2000 -h
# Where args are Match, Mismatch, Delta, PM, PI, Minscore, MaxPeriod, [options]
# Output: genome.fa.2.6.6.80.10.50.2000.dat
```

### Convert .dat file to gff3

Here are three examples of how you can use `trf2gff` to process a `trf` .dat file

```bash
# Option 1:
# Read from infile and write gff to default outfile
trf2gff -i genome.fa.2.6.6.80.10.50.2000.dat
# Output: genome.fa.2.6.6.80.10.50.2000.gff3

# Option 2:
# Read input from stdin and write to stdout
trf2gff -o - < genome.fa.2.6.6.80.10.50.2000.dat > genome.gff3
# Output: genome.gff3

# Option 3:
# Read from stdin and write to file
trf2gff -o genome.gff3 < genome.fa.2.6.6.80.10.50.2000.dat
# Output: genome.gff3
```

### Extract annotated tandem-repeat features

Use `bedtools getfasta` to extract trf features from genome.

```bash
bedtools getfasta -fi genome.fa -bed genome.gff3
```
