"""

Helper functions

"""

def load_sheet(filename):
    """
    **Purpuse**
        Load the Illumina-style SampleSheet (Same format as for bcl2fastq)
        
        # expected format (csv):
        FCID	Lane	SampleID	SampleRef	Index	Description	Control	Recipe	Operator	SampleProject
        000000000-A8WTD	1	A1	hg19	TAAGGCGA-TAGATCGC	NA	N	NA	NA	cordblood_run1
    
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
    return(res)

def generate_mismatches(seq, num_mismatch):
    """
    **Arguments**
        a sequence
    """
    assert "N" not in seq, "Cannot have 'N' base pairs in the starting index" 
    res = []
    
    for idx, bp in enumerate(seq):
        l = seq[0:idx]
        r = seq[idx+1:]
        print idx, seq, l + "N" + r
    return(res)
        
def populate_table(sample_sheet, num_mismatch):
    """
    **Purpose**
        populate the dictionary table for sampleID and indices for a set of mismatches
    
    **Arguments**
        sample_sheet
            the output from load_sheet, i.e a dict of {"sampleID": "index" ... }
            
        num_mismatches 
        
    """
    res = {}
    
    for k in sample_sheet:
        res[k] = []
        res[k].append(sample_sheet[k])
        res[k] + generate_mismatches(sample_sheet[k], num_mismatch)
    
    sanity_check_table(res)
    return(res)
    
def sanity_check_table(pop_table):
    """
    **Purpose**
        check the population table for collisions.
        
    **Arguments**
        pop_table
            the output from populate_table()
    """
    pass

def fast_matcher(seq1, seq2):
    """
    Some restrictions
    
    1. Must be the same length.
    2. Does not check revcomp
    """
    pass

if __name__ == "__main__":
    sample_sheet = load_sheet("SampleSheet_run1.csv")
    print populate_table(sample_sheet, 2)
        