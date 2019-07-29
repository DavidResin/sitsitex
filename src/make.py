import os, PyPDF2
from python import song_helpers as sh

aux_dir = "aux_files"
out_dir = "output"

print("@@@ Processing songs")
print()

fn = "registry"

try:
	sh.generate_song_file(os.path.join("data", "song_files"), reg_fn=fn)

except:
	if False:
		to_check = "! I can't write on file `" + fn + ".pdf'."

		with open(fn + ".log", "r") as f:
			if to_check in f.read().splitlines():
				print("ERROR")
				print("You need to close '" + fn + ".pdf' before you can recompile it.")
				print("Some PDF readers block files while they are open.")



	# What about ! pdfTeX error (font expansion): auto expansion is only possible with scalable 

	# What about :! Package datatool Error: No row found in database `mydata' for column `1' matc
	#hing `en_eurovisionCH'.

	# line break happens for real

	# only open log if exists

print("@@@ Printing sequential PDF")
print()

# GENERATE (TAKE CARE THAT THE TOC IS READ AT THE 2ND TIME)
for i in range(2):
	doc.generate_pdf(filepath=path, compiler='pdflatex', clean=True)

with open("songbook.pdf", "rb") as f:
	pdf = PyPDF2.PdfFileReader(f)
	pages = pdf.trailer["/Root"]["/Pages"]["/Count"]

sheets = (pages + 3) / 4
seqs = [[pages - x, x + 1, x + 2, pages - x - 1] for x in range(0, 2 * sheets, 2)]
ids = [item for sub in seqs for item in sub]
order = ",".join(ids)

print("@@@ Printing booklet (" + pages + " pages, " + sheets + " sheets)")
print()

# GENERATE

print("@@@ Moving output files")
print()

for fn in ["songbook.pdf", "booklet.pdf"]
	aux_path = os.path.join(aux_dir, fn)
	out_path = os.path.join(out_dir, fn)

	if os.path.exists(out_path):
		os.remove(out_path)

	os.rename(aux_path, out_path)
	
print("@@@ Done")