## Python script to take a subset of samples and perform an inverse normal rank transformation on phenotype values

import sys
import os
import pandas
import numpy

from scipy.stats import norm, rankdata

raw_phenos = sys.argv[1] # tab=delimited file with untransformed phentype data
phenotype_list = sys.argv[2] # List of phentyoes to transform
sample_list = sys.argv[3] # list of samples (FID and IID) to retain
int_phenos = sys.argv[4] # file to write the transformed phnotype data to
pheno_index = sys.argv[5] # filename for creating the index of phentypes and columns for conditional analysis

def rank_normalise(rank, data_len):
	r_norm = norm.ppf((rank - 0.5)/(data_len))
	return r_norm

def rank_int(values):
	rank = rankdata(values, method="ordinal")
	ranked_data = pandas.Series(rank, index=values.index)
	transformed = ranked_data.apply(rank_normalise, args=(len(ranked_data),))
	return transformed

pheno_list = []
with open(phenotype_list, "r") as pheno_file:
	for line in pheno_file:
		pheno_name = line.strip()
		pheno_list.append(pheno_name)

pop_sample_data = pandas.read_table(sample_list, delim_whitespace=True, header=None, names=["FID", "IID"])

raw_pheno_data = pandas.read_table(raw_phenos, delim_whitespace=True)

pop_pheno_data = pandas.merge(pop_sample_data, raw_pheno_data, on=["FID", "IID"]).reset_index(drop=True)
sample_data = pop_pheno_data.iloc[:,0:2]
pheno_data = pop_pheno_data.iloc[:,2:]

for column in pheno_data:
	if column in pheno_list:
		print column
		int_pheno = rank_int(pheno_data[column])
		new_column_name = column + "_int"
		sample_data[new_column_name] = int_pheno
		
sample_data.to_csv(int_phenos, sep="\t", header=True, index=False)
headers = list(sample_data.columns.values)
phenos = headers[2:]

with open(pheno_index, "w") as index_file:
	for pheno_name in phenos:
		col_index = phenos.index(pheno_name)
		index_file.write(pheno_name + "\t" + str(col_index + 1) + "\n")
	