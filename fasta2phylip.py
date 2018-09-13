## convert aligned fasta to phylip sequential

import sys
import os
import re

fasta_file = sys.argv[1]

work_dir = os.path.dirname(fasta_file)
basename = os.path.basename(fasta_file)
file_basename = basename.rsplit(".", 1)[0]

outfile_name = file_basename + ".phy"
outfile = os.path.join(work_dir, outfile_name)

seq_dict = {}

seq_length = 0
seq_count = 0

with open(fasta_file, "r") as infile:
	for block in re.split("^>", infile.read(), flags=re.MULTILINE):
		if block:
			seq_count += 1
			seq_block = block.split("\n")
			if seq_block[0] != "":
				header = seq_block[0]
				sequence = ""
				for line in seq_block[1:]:
					sequence += line.strip()
				seq_length = len(sequence)
				seq_dict[header] = sequence

with open(outfile, "w") as phylip_file:
	phylip_file.write("{0}\t{1}\n".format(seq_count, seq_length))
	for seq_id, sequence in seq_dict.iteritems():
		phylip_file.write("{0}\t{1}\n".format(seq_id, sequence))