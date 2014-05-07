#!/usr/bin/env python
"""

Demuxy

"""


from operator import itemgetter
import sys, os, argparse, logging, random, time, subprocess, copy, numpy, itertools

# demuxy modules
import config
import lib
import progress

splurge = """
    demuxy is a tool to demultiplex Illumina sequencing data\n
    It takes a much more aggressive approach to demultiplexing the data 
    by taking the maximum distances between each index up to some
    specified limit.
    \n\n
    Version: %s""" % config.version

parser = argparse.ArgumentParser(description=splurge)
parser.add_argument("-1", "--p1", help="paired-end 1 fastq file (Required)", required=True)
parser.add_argument("-2", "--p2", help="paired-end 2 fastq file (Required)", required=True)
parser.add_argument("-s", "--sheet", help="The Illumina-style SampleSheet (Required)", required=True)
parser.add_argument("-m", "--mismatch", help="Maximum number of mismatches in indeces (Required)", required=True, type=int)
parser.add_argument("-z", "--opt", help="Profile the code for optimisation")

def do(null=None):  
    sample_sheet = lib.load_sheet(args.sheet)
    table = lib.populate_table(sample_sheet, args.mismatch) # 5 is the point for the first mismatch
    
    # open the output files:
    files = {k: open("%s.fq" % k, "w") for k in sample_sheet.keys()}
    counts = {i: 0 for i in sample_sheet.keys()}
    
    n = 0
    m = 0
    tot_tags = 0

    for fq1, fq2 in lib.fastqPE(args.p1, args.p2):
        index = fq1["name"].split(":")[-1]
        # match the index against the table
        for k in table:
            if index in table[k]:
                counts[k] += 1
                files[k].write("%s\n%s\n%s\n%s\n" % (fq1["name"], fq1["seq"], fq1["strand"], fq1["qual"]))
                files[k].write("%s\n%s\n%s\n%s\n" % (fq2["name"], fq2["seq"], fq2["strand"], fq2["qual"]))
                break
        
        tot_tags += 1
        n += 1
        if n > 1e6:
            m += 1
            n = 0
            config.log.info("Did %sM tags" % m)
    
    for k in counts:
        config.log.info("Found %s tags for sample %s" % (counts[k], k))
    sum_counts = sum(counts.values())
    config.log.info("Able to rescue %s tags from %s total (%%%.2f)" % (sum_counts, tot_tags, (sum_counts/float(tot_tags))*100.0))
    return

if __name__ == "__main__":    
    s = time.time() # so tmp files all get the same time
    args = parser.parse_args()
    config.log.info("demuxy, version: %s" % config.version)
    config.log.info("Starting on %s" % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))   

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