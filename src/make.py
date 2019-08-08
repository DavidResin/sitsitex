import os, PyPDF2
from python import song_helpers as sh

aux_dir = "aux_files"
out_dir = "outputs"
file = "songbook.tex"

# Options:
### No song compilation
### Force song compilation
### No booklet
### Flush aux_files
### custom output folder
### verbose option (0=full, 1=warnings&errors, 2=errors only (default), 3=silent)
### special options for single actions? (song compil, test packages)
### version
### custom name

print()
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
				print("Some PDF readers make files read-only while they are open.")



	# What about ! pdfTeX error (font expansion): auto expansion is only possible with scalable 

	# What about :! Package datatool Error: No row found in database `mydata' for column `1' matc
	#hing `en_eurovisionCH'.

	# line break happens for real

	# only open log if exists

print()
print("@@@ Printing sequential PDF")
print()

# GENERATE (TAKE CARE THAT THE TOC IS READ AT THE 2ND TIME)
# GOTTA CLEAN THE NAMING OF FILES (DYNAMIC OR STATIC?)
# CHECKSUM FOR CHANGES
# USE latexmk IF AVAILABLE OTHERWISE USE pdflatex
# AUTO songs.sty INSTALL?
# MESSAGES SAYING WHAT'S MISSING
os.system(f"latexmk -quiet -outdir={ aux_dir } -pdf { file }")

with open(aux_dir + "/songbook.pdf", "rb") as f:
	pdf = PyPDF2.PdfFileReader(f)
	pages = pdf.trailer["/Root"]["/Pages"]["/Count"]

sheets = int((pages + 3) / 4)
seqs = [[4 * sheets - x, x + 1, x + 2, 4 * sheets - x - 1] for x in range(0, 2 * sheets, 2)]
ids = [str(item) for sub in seqs for item in sub]
order = ",".join(ids)

print()
print(f"@@@ Printing booklet ({ pages } pages, { sheets } sheets)")
print()

os.system(f'''pdflatex \
			-interaction=batchmode \
			-output-directory={ aux_dir } \
			-jobname="booklet" \
			"\\def\\sso{{{ order }}} \\def\\ssf{{{ aux_dir }/songbook.pdf}} \\input{{booklet.tex}}"''')

print()
print("@@@ Moving output files")
print()

for fn in ["songbook.pdf", "booklet.pdf"]:
	aux_path = os.path.join(aux_dir, fn)
	out_path = os.path.join(out_dir, fn)

	# Need to remove fls file

	if os.path.exists(aux_path):
		if os.path.exists(out_path):
			os.remove(out_path)

		os.rename(aux_path, out_path)
	
print()
print("@@@ Done")
print()