# Standard libraries
import argparse, os, shutil, sys, textwrap
from argparse import RawTextHelpFormatter

# External libraries
import latexmake, PyPDF2

# Local scripts
from ._version import __version__

def setup_ap():
	ap = argparse.ArgumentParser(description=f"SitsiTeX { __version__ } - List of arguments", formatter_class=RawTextHelpFormatter)
	ap.add_argument("-n", "--name", 	type=str,	default=None, 			help="Custom name for output files, i.e. '<name>_songbook.pdf'")
	ap.add_argument("-V", "--version", 				action='version',		help="Show the version number", 				version=__version__)
	ap.add_argument("-a", "--abort-on-error",		action="store_true",	help="Abort on non-critical errors")
	ap.add_argument("-f", "--flush", 				action="store_true", 	help="Flush auxiliary files")
	out_grp = ap.add_mutually_exclusive_group()
	out_grp.add_argument("-q", "--quiet", 			action="store_const", 	dest="verbose",	const="0", 		default="1",	help="No console output")
	out_grp.add_argument("-v", "--verbose", 		action="store_const", 	dest="verbose",	const="2", 						help="Exhaustive console output")
	act_grp = ap.add_mutually_exclusive_group()
	act_grp.add_argument("-t", "--test",			action="store_const", 	dest="action",	const="test",	default="all",	help="Unit tests")
	act_grp.add_argument("-oc", "--only-compil", 	action="store_const", 	dest="action",	const="only-compil",			help="Only compile songs")
	act_grp.add_argument("-os", "--only-songbook", 	action="store_const", 	dest="action",	const="only-songbook",			help="Only generate songbook")
	act_grp.add_argument("-ob", "--only-booklet", 	action="store_const", 	dest="action",	const="only-booklet",			help="Only generate booklet")
	act_grp.add_argument("-of", "--only-flush", 	action="store_const", 	dest="action",	const="only-flush",				help="Only flush auxiliary files")
	act_grp.add_argument("-nb", "--no-booklet", 	action="store_const", 	dest="action",	const="no-booklet",				help="Skip the booklet generation")
	ap.add_argument("-c", "--compil", 	type=int, 
										default=1,
										metavar="CODE",
										choices=[0, 1, 2],
										help=textwrap.dedent("Controls the compilation of song files:\n"
															+ "- 0 : no compilation\n"
															+ "- 1 : compile only the files that changed (default)\n"
															+ "- 2 : compile everything"))

	return ap

def parse_args(ap):
	args = vars(ap.parse_args())

	# Recover arguments
	name = args["name"]
	flush = args["flush"]
	abort = args["abort_on_error"]
	verbose = args["verbose"]
	compil = args["compil"]
	action = args["action"]

	# Clear arguments
	sys.argv = [sys.argv[0]]

	# Setup flags
	flags = dict.fromkeys(["compil", "songbook", "booklet", "flush"], int(action in ["all", "no-booklet"]))
	el = ap._option_string_actions.get("--" + action)

	if action == "all":
		flags["flush"] = int(flush)
	elif action == "no-booklet":
		flags["booklet"] = 0
	elif action == "test":
		print("SYSTEM: Testing calls have not been implemented yet")
		sys.exit(0)
	else:
		flags[action.split("only-")[1]] = 1

	flags["compil"] = compil if flags["compil"] else 0

	# Write opener
	opener = f"Running SitsiTeX { __version__ } - "
	opener += el.help if el else "Full cycle"

	parsed = {
		"opener" : opener,
		"flags" : flags,
		"verbose" : verbose,
		"abort" : abort,
		"name" : name
	}

	return parsed

def make_songbook(fn, ltx_dir, aux_dir, keep):
	# Memorize current directory
	base_dir = os.getcwd()

	# Change to latex directory
	os.chdir(ltx_dir)

	# Run latexmake script
	sys.argv += [fn + ".tex"]
	latexmake.main()

	# Move output files to aux_dir
	for fn in os.listdir():
		if os.path.isfile(fn):
			if not any([fn.endswith(k) for k in keep]):
				old_path = os.path.join(os.getcwd(), fn)
				new_path = os.path.join(os.getcwd(), aux_dir, fn)
				shutil.move(old_path, new_path)

	# Change back to original directory
	os.chdir(base_dir)

def get_pdf_data(path):
	# Get number of pages
	with open(path, "rb") as f:
		pdf = PyPDF2.PdfFileReader(f)
		pages = pdf.trailer["/Root"]["/Pages"]["/Count"]

	# Compute order and number of sheets
	sheets = int((pages + 3) / 4)
	seqs = [[4 * sheets - x, x + 1, x + 2, 4 * sheets - x - 1] for x in range(0, 2 * sheets, 2)]
	ids = [str(item) for sub in seqs for item in sub]
	order = ",".join(ids)

	pdf_data = {
		"pages" : pages,
		"sheets" : sheets,
		"order" : order
	}

	return pdf_data

def make_booklet(src_fn, dst_fn, ltx_dir, aux_dir, order):
	# Memorize current directory
	base_dir = os.getcwd()

	# Change to latex directory
	os.chdir(ltx_dir)

	# Run pdflatex
	os.system(f'''pdflatex \
				-interaction=batchmode \
				-output-directory={ aux_dir } \
				-jobname="{ dst_fn }" \
				"\\def\\sso{{{ order }}} \\def\\ssf{{{ aux_dir }"/"{ src_fn }.pdf}} \\input{{{ dst_fn }.tex}}"''')

	# Change back to original directory
	os.chdir(base_dir)

def move_output(fns, src_dir, dst_dir, name=None):
	prefix = name + "_" if name else ""

	for fn in fns:
		tmp = fn + ".pdf"
		src_path = os.path.join(src_dir, tmp)
		dst_path = os.path.join(dst_dir, prefix + tmp)

		shutil.move(src_path, dst_path)

def flush_dir(path="", keep=[]):
	count = 0

	for fn in os.listdir(path):
		if fn not in keep:
			file = os.path.join(path, fn)

			try:
				os.remove(file)
			except IsADirectoryError:
				print(f"Path '{ file }' is a directory and will not be removed for safety reasons.")
			except FileNotFoundError:
				print(f"File '{ file }' does not exist.")
			except Exception:
				print(f"File '{ os.path.join(path, fn) }' is open somewhere and thus cannot be deleted.")
			else:
				count += 1

	return count
