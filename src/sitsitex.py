import latexmake, os, shutil, sys, PyPDF2
from python import song_helpers as sh

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

base_dir = os.getcwd()
ltx_dir = "latex"
aux_dir = "aux_files"
out_dir = "outputs"
dat_dir = "data"
pyt_dir = "python"
file = "songbook.tex"
reg_fn = "registry"
to_keep = ["tex", "sty", "dat"]
gitkeep = ".gitkeep"

# Check if directories are missing
for d in [ltx_dir, dat_dir, pyt_dir, out_dir]:
	if d not in os.listdir():
		sys.exit(f"Directory '{ d }' not found, program cannot proceed.")

print()
print("@@@ Processing songs")
print()

try:
	sh.generate_song_file(path_in=os.path.join(dat_dir, "song_files"), path_out="latex", reg_fn=reg_fn)
except:
	if False:
		to_check = "! I can't write on file `" + reg_fn + ".pdf'."

		with open(reg_fn + ".log", "r") as f:
			if to_check in f.read().splitlines():
				print("ERROR")
				print("You need to close '" + reg_fn + ".pdf' before you can recompile it.")
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
# CHECKSUM FOR CHANGES, OR JUST CHECK LAST MODIF TIME
# AUTO songs.sty INSTALL?
# MESSAGES SAYING WHAT'S MISSING

# Run latexmake script
os.chdir(ltx_dir)
sys.argv += [file]
latexmake.main()

# Move output files to aux_dir
for fn in os.listdir():
	if os.path.isfile(fn):
		if not any([fn.endswith(tk) for tk in to_keep]):
			shutil.move(os.path.join(os.getcwd(), fn), os.path.join(os.getcwd(), aux_dir, fn))

# Find the number of pages
with open(os.path.join(aux_dir, "songbook.pdf"), "rb") as f:
	pdf = PyPDF2.PdfFileReader(f)
	pages = pdf.trailer["/Root"]["/Pages"]["/Count"]

sheets = int((pages + 3) / 4)
seqs = [[4 * sheets - x, x + 1, x + 2, 4 * sheets - x - 1] for x in range(0, 2 * sheets, 2)]
ids = [str(item) for sub in seqs for item in sub]
order = ",".join(ids)

# NEED TO DEAL WITH CASES WHERE NUMPAGES % 4 != 0

print()
print(f"@@@ Printing booklet ({ pages } pages, { sheets } sheets)")
print()

os.system(f'''pdflatex \
			-interaction=batchmode \
			-output-directory={ aux_dir } \
			-jobname="booklet" \
			"\\def\\sso{{{ order }}} \\def\\ssf{{{ aux_dir }"/songbook.pdf}} \\input{{booklet.tex}}"''')

os.chdir(base_dir)

print()
print("@@@ Moving output files")
print()

for fn in ["songbook.pdf", "booklet.pdf"]:
	aux_path = os.path.join(ltx_dir, aux_dir, fn)
	out_path = os.path.join(out_dir, fn)

	# Need to remove fls file

	if os.path.exists(aux_path):
		if os.path.exists(out_path):
			os.remove(out_path)

		os.rename(aux_path, out_path)
	
print()
print("@@@ Done")
print()