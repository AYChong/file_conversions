## Script to check for duplicate SNP IDs in 

## Uses python 2.7.11 on Rescomp
## Run on short.qc 

import sys
import os
import pandas
import numpy

infile = sys.argv[1] # input file to check for duplicates
outfile = sys.argv[2] # output file with duplicates removed

with open(outfile, "w") as blank_file:
	blank_file.truncate()

raw_data = pandas.read_table(infile, delim_whitespace=True, header=None, chunksize=10000)

if infile.endswith(".info"):
	print "info file"
	for chunk in raw_data:
		clean_data = chunk.drop_duplicates(0, keep="first", inplace=False)
		clean_data.to_csv(outfile, mode="a", sep="\t", header=False, index=False)
elif infile.endswith(".gen"):
	print "gen file"
	for chunk in raw_data:
		num_cols = len(chunk.columns)
		sample_cols = num_cols - 5
		if sample_cols % 3 == 0:
			clean_data = chunk.drop_duplicates(0, keep="first", inplace=False)
			clean_data.to_csv(outfile, mode="a", sep="\t", header=False, index=False)
		elif sample_cols % 3 == 1:
			geno_data = chunk.iloc[:,1:] ## Assumes 1st column is chromosome number
			geno_data.columns = numpy.arange(len(geno_data.columns))
			clean_data = geno_data.drop_duplicates(0, keep="first", inplace=False)
			clean_data.to_csv(outfile, mode="a", sep="\t", header=False, index=False)
		else:
			print "Unknown columns. .gen file may be incorrectly formatted"
			print chunk.iloc[0:1,0:10]
			sys.exit()
else:
	print "unrecognised file type"
	print infile
	sys.exit()

