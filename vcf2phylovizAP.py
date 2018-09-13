# Convert phased vcf genotype data to allelic profile data for phyloviz

import sys
import csv

infile = sys.argv[1]
outfile = sys.argv[2]


## retrieve VCF header info
headers = []
sample_ids = []
snp_list = []
sequence_dict = {}
with open(infile, "r") as vcf, open(outfile, "wb") as ap:
	writer = csv.writer(ap, delimiter="\t")
	for line in vcf:
		if line.startswith("##"): # Skip info lines
			pass
		elif line.startswith("#CHROM"):
			headers.extend(line.strip().split())
			sample_ids.extend(line.strip().split()[9:])
			for sample_id in sample_ids:
				hap_a = sample_id + "_1"
				hap_b = sample_id + "_2"
				sequence_dict[hap_a] = []
				sequence_dict[hap_b] = []
		else: # read in genotype data from vcf file
			try:
				snp_data = line.strip().split()
				snp_set = set()
				alleles = [snp_data[3]]
				alleles.extend(snp_data[4].split(","))
				snp_id = snp_data[2]
				maxlen = len(max(alleles, key=len))
				padded_alleles = [x.rjust(maxlen, "-") for x in alleles] # Adds alignment gaps to deal with indels ## Need to check how indels are dealt with?
				genotype_list = snp_data[9:]
				for genotype_call in genotype_list:
					gen_a, gen_b = genotype_call.split("|")
					if not gen_a == ".": # ignore missing values as they are treated as wildcards and therefore not informative to determine haplotype relatedness
						snp_set.update(gen_a)
					if not gen_b == ".":
						snp_set.update(gen_b)
				if len(snp_set) > 1: # Position is variable and therefore informative for haplotype relatedness
					snp_list.append(snp_id)
					counter = 0
					for genotype_call in genotype_list:
						sample_id = sample_ids[counter]
						hap_a = sample_id + "_1"
						hap_b = sample_id + "_2"
						gen_a, gen_b = genotype_call.split("|")
						if gen_a == ".": # Add placeholder for missing values
							allele_a = "X" * maxlen
						else:
							allele_a = padded_alleles[int(gen_a)]
						if gen_b == ".":
							allele_b = "X" * maxlen
						else:
							allele_b = padded_alleles[int(gen_b)]
						sequence_dict[hap_a].append(allele_a)
						sequence_dict[hap_b].append(allele_b)
						counter += 1
				else:
					pass
			except:
				print line
				continue

print len(snp_list), "SNP IDs included in the alignment file:"
print ", ".join(x for x in snp_list)

with open(outfile, "w") as fasta:
	for hap_id, alleles in sorted(sequence_dict.iteritems()):
		header = ">" + hap_id
		sequence = "".join(x for x in alleles)
		fasta.write(header + "\n" + sequence + "\n")
		#print hap_id, len(sequence)


