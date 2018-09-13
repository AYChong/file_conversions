import sys
import cPickle
import csv


gtf_file = sys.argv[1]
out_file = sys.argv[2]

#######################################

keep_list = ["gene", "CDS", "start_codon", "stop_codon", "five_prime_utr", "three_prime_utr", "exon"]

with open(gtf_file, "r") as gtf, open(out_file, "wb") as table_file:
	writer = csv.writer(table_file, delimiter="\t")
	for line in gtf:
		if not line.startswith("#"):
			chromosome, source, type, start, end, score, strand, frame, attributes = line.strip().split("\t")
			if type in keep_list: # filters out additional annotations
				gene_id = "N/A"
				gene_name = "N/A"
				attribute_list = attributes.split("; ")
				for attribute in attribute_list:
					if attribute.startswith("gene_id"):
						gene_id = attribute.split(None, 1)[1]
					elif attribute.startswith("gene_name"):
						gene_name = attribute.split(None, 1)[1]
				writer.writerow([chromosome, type, start, end, gene_id, gene_name])