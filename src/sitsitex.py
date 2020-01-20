# Standard libraries
import json, os, shutil, sys

# Local scripts
from python.scripts import parse, logger, steps

# run "py.test python/test" to run tests

# keep default name files in aux
# compile songmaster version at the same time (requires new features)
# songbook memory (kinda exists de facto)

	# What about ! pdfTeX error (font expansion): auto expansion is only possible with scalable 

	# What about :! Package datatool Error: No row found in database `mydata' for column `1' matc
	#hing `en_eurovisionCH'.

	# line break happens for real

	# only open log if exists

# GENERATE (TAKE CARE THAT THE TOC IS READ AT THE 2ND TIME)
# GOTTA CLEAN THE NAMING OF FILES (DYNAMIC OR STATIC?)
# CHECKSUM FOR CHANGES, OR JUST CHECK LAST MODIF TIME
# AUTO songs.sty INSTALL?
# MESSAGES SAYING WHAT'S MISSING
# NEED TO DEAL WITH CASES WHERE NUMPAGES % 4 != 0

# Constants
ltx_dir = "latex"
aux_dir = "aux_files"
out_dir = "outputs"
dat_dir = "data"
pyt_dir = "python"

sb_fn = "songbook"
bl_fn = "booklet"
reg_fn = "registry"
cfg_fn = "config"
gitkeep = ".gitkeep"

to_keep = ["tex", "sty", "dat"]
to_move = []

# Check if directories are missing
for d in [ltx_dir, dat_dir, pyt_dir, out_dir]:
	if d not in os.listdir():
		sys.exit(f"Directory '{ d }' missing, program cannot proceed.")

# Get config data
try:
	with open(cfg_fn + ".json", "r") as file:
		config = json.load(file)
except:
	sys.exit("Config file not found, program cannot proceed.")

# Argument parsing
ap = steps.setup_ap()
parsed = steps.parse_args(ap)

# "opener" : opener, -> print
# "flags" : flags, -> select what part of the code is run or not
# "verbose" : verbose, -> for the logger
# "abort" : abort, -> choose exception behavior
# "name" : name -> final file name

log = logger.Logger()

print(parsed["opener"])

if parsed["flags"]["compil"] > 0:

	print()
	print("@@@ Processing songs")
	print()

	try:
		parse.generate_song_file(path_in=os.path.join(dat_dir, "song_files"), path_out="latex", reg_fn=reg_fn)
	except:
		if False:
			to_check = "! I can't write on file `" + reg_fn + ".pdf'."

			with open(reg_fn + ".log", "r") as f:
				if to_check in f.read().splitlines():
					print("ERROR")
					print("You need to close '" + reg_fn + ".pdf' before you can recompile it.")
					print("Some PDF readers make files read-only while they are open.")

if parsed["flags"]["songbook"] > 0:

	print()
	print("@@@ Printing songbook")
	print()

	# contextlib.redirect_stdout

	# Make the songbook
	steps.make_songbook(fn=sb_fn, ltx_dir=ltx_dir, aux_dir=aux_dir, keep=to_keep)
	to_move += [sb_fn]

if parsed["flags"]["booklet"] > 0:

	# Get pdf metadata
	pdf_data = steps.get_pdf_data(os.path.join(ltx_dir, aux_dir, sb_fn + ".pdf"))

	print()
	print(f"@@@ Printing booklet ({ pdf_data['pages'] } pages, { pdf_data['sheets'] } sheets)")
	print()

	# Make the booklet
	steps.make_booklet(src_fn=sb_fn, dst_fn=bl_fn, ltx_dir=ltx_dir, aux_dir=aux_dir, order=pdf_data["order"])
	to_move += [bl_fn]

if to_move:

	print()
	print("@@@ Moving output files")
	print()

	# Need error management

	# Move output files and add prefix if provided
	steps.move_output(fns=to_move, src_dir=os.path.join(ltx_dir, aux_dir), dst_dir=out_dir, name=parsed["name"])

if parsed["flags"]["flush"] > 0:

	print()
	print("@@@ Flushing auxiliary files")
	print()

	# Flush auxiliary files
	steps.flush_dir(path=os.path.join(ltx_dir, aux_dir), keep=[gitkeep])

print()
print("@@@ Done")
print()