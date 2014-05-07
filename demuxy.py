#!/usr/bin/env python
"""

Demuxy

"""


from operator import itemgetter
import sys, os, argparse, logging, random, time, subprocess, copy, progress, numpy, itertools

import config

parser = argparse.ArgumentParser(description="""demuxy is a tool to demultiplex Version: %s""" % config.version)
parser.add_argument("-1", "--p1", help="paired-end 1 fastq file (Required)", required=True)
parser.add_argument("-2", "--p2", help="paired-end 2 fastq file (Required)", required=True)
parser.add_argument("-s", "--sheet", help="(Required)", required=True)
parser.add_argument("--mismatch1", help="Maximum number of mismatches in index1 (Required)", required=True)
parser.add_argument("--mismatch2", help="Maximum number of mismatches in index2 (Required)", required=True)
parser.add_argument("-o", "--output", default="unaligned_.tsv", help="output filename, reads will be split into _R1 and _R2 files (default: unaligned_.tsv)")

def do(null=None):  
    pass

if __name__ == "__main__":
    do()