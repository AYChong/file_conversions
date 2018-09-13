# Script to merge chunked MACh files into single chromosome files

import sys
import os
import pandas
import csv
import tempfile
import shutil

chunk_map = sys.argv[1] # Map file for each of the chromosome chunks
chunk_dir = sys.argv[2] # directory containing the chunked MACH files
mach_dir = sys.argv[3] # directory to save the chromosomal MACH files
mach_prefix = sys.argv[4] # prefix for naming the chromosomal MACH files

dosefile = os.path.join(mach_dir, mach_prefix + ".machdose.gz")
infofile = os.path.join(mach_dir, mach_prefix + ".machinfo.gz")
legendfile = os.path.join(mach_dir, mach_prefix + ".machlegend.gz")

tmpdose = tempfile.NamedTemporaryFile(mode="a", dir=chunk_dir, delete=False)
tmpinfo = tempfile.NamedTemporaryFile(mode="a", dir=chunk_dir, delete=False)
tmplegend = tempfile.NamedTemporaryFile(mode="a", dir=chunk_dir, delete=False)

with open(chunk_map, "r") as map_file:
	for line in map_file:
		chromosome, start, end, chunk_name, counter = line.strip().split()
		chunk_dosefile = os.path.join(chunk_dir, counter + ".machdose")
		chunk_infofile = os.path.join(chunk_dir, counter + ".machinfo")
		chunk_legendfile = os.path.join(chunk_dir, counter + ".machlegend")
		
		if os.path.exists(chunk_dosefile):
			chunk_dose_data = pandas.read_table(chunk_dosefile, delim_whitespace=True, header=None)
			chunk_dose_data.to_csv(tmpdose.name, mode="a", sep="\t", na_rep="NA", header=False, index=False, compression="gzip")
		
			chunk_info_data = pandas.read_table(chunk_infofile, delim_whitespace=True)
			chunk_info_data.to_csv(tmpinfo.name, mode="a", sep="\t", na_rep="NA", index=False, compression="gzip")
			
			chunk_legend_data = pandas.read_table(chunk_legendfile, delim_whitespace=True)
			chunk_legend_data.to_csv(tmplegend.name, mode="a", sep="\t", na_rep="NA", index=False, compression="gzip")

shutil.move(tmpdose.name, dosefile)
shutil.move(tmpinfo.name, infofile)
shutil.move(tmplegend.name, legendfile)