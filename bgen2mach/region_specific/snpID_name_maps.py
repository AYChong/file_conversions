## Create a dictionary to map SNP_IDs used for GCTA to rsIDs for LocusZoom plots

## Uses python 2.7.11 on Rescomp 

import sys
import os
import pandas
import cPickle

stats_file = sys.argv[1]
mach_dir = sys.argv[2] # directory to save the chromosomal MACH files
mach_prefix = sys.argv[3] # prefix for naming the chromosomal MACH files

dictfile = os.path.join(mach_dir, mach_prefix + ".snpmap.dict")
txt_file = os.path.join(mach_dir, mach_prefix + ".snpmap.txt")


snp_data = pandas.read_table(stats_file, delim_whitespace=True, comment="#", usecols=["alternate_ids", "rsid"])
snp_ids = snp_data.set_index("alternate_ids")["rsid"].to_dict()


with open(dictfile, "wb") as outfile:
	cPickle.dump(snp_ids, outfile, 1)

with open(txt_file, "w") as outfile2:
	outfile2.write("SNP_ID" + "\t" + "rsID" + "\n")
	for snp, rsid in snp_ids.iteritems():
		outfile2.write(snp + "\t" + rsid + "\n")