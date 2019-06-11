import os
from python import song_helpers as sh

fn = "registry"

try:
	sh.generate_song_file(os.path.join("data", "song_files"), reg_fn=fn)
except:
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