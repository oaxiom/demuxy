usage: demuxy.py [-h] -1 P1 -2 P2 -s SHEET -m MISMATCH [-z OPT]

demuxy is a tool to demultiplex Illumina sequencing data It takes a much more
aggressive approach to demultiplexing the data by taking the maximum distances
between each index up to some specified limit. Version: 0.9

optional arguments:
  -h, --help            show this help message and exit
  -1 P1, --p1 P1        paired-end 1 fastq file (Required)
  -2 P2, --p2 P2        paired-end 2 fastq file (Required)
  -s SHEET, --sheet SHEET
                        The Illumina-style SampleSheet (Required)
  -m MISMATCH, --mismatch MISMATCH
                        Maximum number of mismatches in indeces (Required)
  -z OPT, --opt OPT     Profile the code for optimisation
