
import sys
import os
import subprocess
import shlex

indir = sys.argv[1]
outdir = sys.argv[2]

for fname in os.listdir(indir):
	if fname.endswith(".vcf.gz"):
		basename = fname.rsplit(".", 2)[0]
		infile = os.path.join(indir, fname)
		outfile = os.path.join(outdir, basename)
		
		qsub_cmd = "qsub /users/hill/achong/Scripts/qsub-plink-vcf.sh {0} {1}".format(infile, outfile)
#		print qsub_cmd
		try:
			args = shlex.split(qsub_cmd)
			qsub = subprocess.Popen(args, stdout=subprocess.PIPE)
			out = qsub.communicate()[0]
			print out.strip()

		except KeyboardInterrupt:
			qsub.kill()
		except Exception as e:
			print e
			sys.exit()
		
	

