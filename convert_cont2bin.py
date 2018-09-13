# Script to convert continuous phenotypes to binary case/control phenotypes based on a list of cutoff thresholds and combine with continuous phenotypes

import sys
import os
import pandas
import numpy

phenotype_file = sys.argv[1]
cutoff_file = sys.argv[2]
converted_file = sys.argv[3]

cutoff_df = pandas.read_table(cutoff_file, delim_whitespace=True, index_col=0)

raw_df = pandas.read_table(phenotype_file, delim_whitespace=True)
sample_df = raw_df.iloc[:,0:2].astype(str)
pheno_df = raw_df.iloc[:,2:].fillna("NA")

tmp_df = pandas.DataFrame()
converted_df = pandas.DataFrame()
for pheno_col in pheno_df:
	cutoff = float(cutoff_df.loc[pheno_col, "suggested_cutoff"])
	converted_col = pheno_col + "_epi"
	tmp_df[converted_col] = numpy.where(pheno_df[pheno_col] > cutoff, 2, 1)
	converted_df[converted_col] = numpy.where(pheno_df[pheno_col].astype(str) == "NA" , "NA", tmp_df[converted_col])

merged_df = pandas.concat([sample_df, pheno_df, converted_df], axis=1).fillna("NA")
merged_df.to_csv(converted_file, sep="\t", header=True, index=False)