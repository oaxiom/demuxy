"""

Helper functions

"""

import config

def load_sheet(filename):
    """
    **Purpuse**
        Load the Illumina-style SampleSheet (Same format as for bcl2fastq)
        
        # expected format (csv):
        FCID    Lane    SampleID    SampleRef   Index   Description Control Recipe  Operator    SampleProject
        000000000-A8WTD 1   A1  hg19    TAAGGCGA-TAGATCGC   NA  N   NA  NA  cordblood_run1
    
        I only want two columns, SampleID and Index
    
    """
    res = {}

    oh = open(filename, "rU")
    for line in oh:
        ll = line.strip().split(",")
        if ll[0] != "FCID":
            sampleID = ll[2]
            index = ll[4].replace("-", "").upper()
            res[sampleID] = index
    config.log.info("Loaded sample sheet '%s'" % filename)
    return(res)

def generate_mismatches(seq, num_mismatch, cdepth=1):
    """
    **Arguments**
        a sequence
    """
    res = []
    
    for idx, bp in enumerate(seq):
        newseq = seq[0:idx] + "N" + seq[idx+1:]
        
        res.append(newseq)
        if cdepth < num_mismatch:
            res = res + generate_mismatches(newseq, num_mismatch, cdepth+1)
    return(res)
        
def populate_table(sample_sheet, num_mismatch):
    """
    **Purpose**
        populate the dictionary table for sampleID and indices for a set of mismatches
    
        The resulting table will be checked for collisions between the mismatches and some advice
        will be given on the maximum possible num_mismatches for these indeces.
    
    **Arguments**
        sample_sheet
            the output from load_sheet, i.e a dict of {"sampleID": "index" ... }
            
        num_mismatches 
            The number of mismatches to consider
            
    """
    res = {}
    
    for k in sample_sheet:
        res[k] = []
        res[k].append(sample_sheet[k])
        res[k] = res[k] + list(set(generate_mismatches(sample_sheet[k], num_mismatch)))
    
    res = cull_collisions(res)
    # convert the table to sets for faster membership testing
    for k in res:
        res[k] = frozenset(res[k])
    
    return(res)
    
def cull_collisions(pop_table):
    """
    **Purpose**
        cull colliding index matches
        
    **Arguments**
        pop_table
            the output from populate_table()
    """
    # First do a quick check to see if there are any colliding members:
    super_table = sum(pop_table.values(), [])
    pre_set_len = len(super_table)
    post_set_len = len(set(super_table))
    
    if pre_set_len == post_set_len: # no collisions, bug out
        config.log.info("There are no collision at this mismatch level")
        config.log.info("Populated table with '%s' combinations" % pre_set_len)
        return(pop_table)    
    
    culled = 0
    scheduled_for_deletion = []
    # we must test each k for collsions
    for k1 in pop_table:
        for k2 in pop_table:
            if k1 != k2:
                # check for collisions between these two pairs:
                seqs1 = set(pop_table[k1])
                seqs2 = set(pop_table[k2])
                union = seqs1 & seqs2
                if union:
                    for s in union:
                        culled += 1
                        # Don't delete here, as it may bias later checks for the presence of this seq
                        scheduled_for_deletion.append(s)
    # Now do the actual deletion:
    for k in pop_table:
        for s in scheduled_for_deletion:
            if s in pop_table[k]:
                idx = pop_table[k].index(s)
                del pop_table[k][idx]

    config.log.info("Culled %s mismatches" % (culled*2,)) # because it is culled from both lists
    config.log.info("Populated table with '%s' combinations" % (pre_set_len-culled*2,))
    return(pop_table)

def fastqPE(filename1, filename2):
    """
    generator object to parse fastQ PE files
    
    @HWI-M00955:51:000000000-A8WTD:1:1101:13770:1659 1:N:0:NNTNNNAGNNCNCTAT
    NGGTAAATGCGGGAGCTCCGCGCGCANNTGCGGCNNNGCATTGCCCATAATNNNNNNNCTACCGACGCTGACTNNNNNCTGTCTCTTATACACATNNNNGAGCCCACGNNNNCNNNCTAGNNNNNNNNNNNNNNNTTCTGCTTGTAAACA
    +
    #,,5,</<-<+++5+568A+6+5+++##5+5++5###+5+55-55A-A--5#######55+5<)+4)43++14#####*1*1*2011*0*1*1*1####***111(/'####/###-(((###############/-(/((./(((((((
    
    """
    oh1 = open(filename1, "rU")
    oh2 = open(filename2, "rU")

    name1 = "dummy"
    while name1 != "":
        name1 = oh1.readline().strip()
        seq1 = oh1.readline().strip()
        strand1 = oh1.readline().strip()
        qual1 = oh1.readline().strip()
        
        name2 = oh2.readline().strip()
        seq2 = oh2.readline().strip()
        strand2 = oh2.readline().strip()
        qual2 = oh2.readline().strip()
        
        res = ({"name": name1, "strand": strand1, "seq": seq1, "qual": qual1},
            {"name": name2, "strand": strand2, "seq": seq2, "qual": qual2})
        yield res   
    return

if __name__ == "__main__":
    sample_sheet = load_sheet("SampleSheet_run1.csv")
    populate_table(sample_sheet, 1) # 5 is the point for the first mismatch

    for i, o in fastqPE("lane1_Undetermined_L001_R1_001.fastq", "lane1_Undetermined_L001_R2_001.fastq"):
        pass