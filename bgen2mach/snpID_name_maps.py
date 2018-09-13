## Create a dictionary to map SNP_IDs used for GCTA to rsIDs for LocusZoom plots

## Uses python 2.7.11 on Rescomp 

import sys
import os
import pandas
import cPickle

chunk_map = sys.argv[1] # Map file for each of the chromosome chunks
chunk_dir = sys.argv[2] # directory containing the chunked MACH files
mach_dir = sys.argv[3] # directory to save the chromosomal MACH files
mach_prefix = sys.argv[4] # prefix for naming the chromosomal MACH files

dictfile = os.path.join(mach_dir, mach_prefix + ".snpmap.dict")
txt_file = os.path.join(mach_dir, mach_prefix + ".snpmap.txt")

snp_ids = {}
with open(chunk_map, "r") as map_file:
	for line in map_file:
		chromosome, start, end, chunk_name = line.strip().split()
		chunk_prefix = chromosome + "." + start + "." + end
		chunk_stat_file = os.path.join(chunk_dir, chunk_prefix + ".snp.stats")
		snp_data = pandas.read_table(chunk_stat_file, delim_whitespace=True, comment="#", usecols=["alternate_ids", "rsid"])
		chunk_snp_ids = snp_data.set_index("alternate_ids")["rsid"].to_dict()
		snp_ids.update(chunk_snp_ids)

with open(dictfile, "wb") as outfile:
	cPickle.dump(snp_ids, outfile, 1)

with open(txt_file, "w") as outfile2:
	outfile2.write("SNP_ID" + "\t" + "rsID" + "\n")
	for snp, rsid in snp_ids.iteritems():
		outfile2.write(snp + "\t" + rsid + "\n")
