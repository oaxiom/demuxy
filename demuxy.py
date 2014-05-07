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
parser.add_argument("-m", "--mismatch", help="Maximum number of mismatches in indeces (Required)", required=True)
parser.add_argument("-o", "--output", default="unaligned_.tsv", help="output filename, reads will be split into _R1 and _R2 files (default: unaligned_.tsv)")

def do(null=None):  
    pass

if __name__ == "__main__":    
    s = time.time() # so tmp files all get the same time
    config.log.info("demuxy, version: %s" % config.version)
    config.log.info("Starting on %s" % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))   
    args = parser.parse_args()

    if args.opt:
        import cProfile, pstats
        cProfile.run("do()", "profile.pro")
        p = pstats.Stats("profile.pro")
        p.strip_dirs().sort_stats("time").print_stats()
    else:
        do()
        
    e = time.time()
    config.log.info("Finishing on %s" % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
    config.log.info("Took %.1f secs, %s mins" % (e-s, int((e-s)/60)))