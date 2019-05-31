import os, re
import markdown as md

# Read markdown song
def from_md(lines):
	# state can be :
	# - 0 (beginning)
	# - 1 (title parsed)
	# - 2 (code parsed)
	# - 3 (subtitle parsed)
	# - 4 (verse parsed)
	state = 0
	song = {"verses" : []}
	invalid = False
	in_verse = False

	patterns = [("_" * i, t) for i, t in zip([3, 2, 1], ['bi', 'b', 'i'])]

	for l in lines:
		l = l.replace("\n", "").strip()

		# Parse title
		if state == 0:
			if l == "":
				print("WARNING: Useless empty line in markdown")
			elif len(l) > 2 and l[:3] == "## ":
				song["title"] = l[2:]
				state = 1
			else:
				invalid = True

		# Parse code
		elif state == 1:
			if l == "":
				print("WARNING: Useless empty line in markdown")
			elif len(l) > 6 and l[:12] == "##### Code: ":
				code = l[12:]
				state = 2
			else:
				invalid = True

		# Parse end of verse or comment to ignore
		elif l == "" or l[0] == ">":
			in_verse = False
			
			if state < 3:
				state = 4

		# Parse subtitle
		elif state == 2 and l[0] == '-':
			if len(l) > 2:
				song["subtitle"] = l[2:]
				state = 3
			else:
				invalid = True

		# Parse verses
		elif state in [2, 3, 4]:
			if not in_verse:
				song["verses"].append([])
				in_verse = True
				state = 4

			parse = md.markdown(l.replace("_", "*"))

			# All asterisks will vanish if the line is valid
			if "*" in parse:
				invalid = True
				continue
			else:
				bold, italic = False, False
				line = []

				elems = [e for e in parse \
					.replace("<", "*<") \
					.replace(">", ">*") \
					.replace("<p>", "") \
					.replace("</p>" ,"").split("*") if len(e)]

				for e in elems:
					if e == "<strong>":
						bold = True
					elif e == "</strong>":
						bold = False
					elif e == "<em>":
						italic = True
					elif e == "</em>":
						italic = False
					else:
						entry = {}

						entry["s"] = ("b" if bold else "") + ("i" if italic else "")
						entry["v"] = e

						line.append(entry)

				song["verses"][-1].append(line)

		else:
			print("ERROR: Illegal state: ", str(state))
			return None

		if invalid:
			print("ERROR: Invalid markdown, please check the style guide")
			print("Line: " + l)
			print("State: " + str(state))
			print(lines)
			return None

	if state == 4:
		return code, song
	else:
		if state == 0:
			missing = "title"
		elif state == 1:
			missing = "code"
		else:
			missing = "verse(s)"

		print("ERROR: Incomplete markdown, " + missing + " missing")
		return None

# Read latex song
def from_latex(lines):
	# state can be :
	# - 0 (beginning)
	# - 1 (waiting for verse)
	# - 2 (in verse)
	# - 3 (end)
	state = 0
	song = {"verses" : []}
	invalid = False

	patterns = [("_" * i, t) for i, t in zip([3, 2, 1], ['bi', 'b', 'i'])]

	for l in lines:
		# Remove useless clutter
		if l[-1] == "\n":
			l = l[:-1]

		if l[-1] == "%":
			l = l[:-1]

		if l[-2:] == "\\\\":
			l = l[:-2]

		l = l.strip()

		# Parse title & code
		if state == 0:
			pat = "^(?P<code>.+) = (?P<title>.+) = {$"
			match = re.match(pat, l)
			
			if bool(match):
				seg = match.groupdict()
				song["title"] = seg["title"]
				code = seg["code"]
				state = 1
			else:
				invalid = True

		# Parse verse start or subtitle
		elif state == 1:
			pat = "^\\\sing{(?P<subtitle>.+)}$"
			match = re.match(pat, l)

			if bool(match):
				seg = match.groupdict()
				song["subtitle"] = seg["subtitle"]
			elif l == "\\verse{":
				song["verses"].append([])
				state = 2
			elif l == "}":
				state = 3
			else:
				invalid = True

		# Parse verse content and end
		elif state == 2:
			if l == "}":
				if len(song["verses"][-1]):
					state = 1
				else:
					invalid = True
			else:
				style = ""
				line = []

				elems = [e for e in l \
					.replace("\\", "*\\") \
					.replace("{", "{*") \
					.replace("}", "*}*").split("*") if len(e)]

				for e in elems:
					if e == "\\textbf{":
						style += "b"
					elif e == "\\textit{":
						style += "i"
					elif e == "}":
						style = style[:-1]
					else:
						entry = {}

						entry["s"] = ("b" if "b" in style else "") + ("i" if "i" in style else "")
						entry["v"] = e

						line.append(entry)

				# Test if all style fields are closed
				if len(style):
					invalid = True
				else:
					song["verses"][-1].append(line)

		# Check for extra lines
		elif state == 3:
			invalid = True
		else:
			print("ERROR: Illegal state: ", str(state))
			return None

		if invalid:
			print("ERROR: Invalid latex, please check the style guide")
			print("Line: " + l)
			print("State: " + str(state))
			return None

	if state == 3:
		return code, song
	else:
		if state == 0:
			missing = "title and code"
		elif state == 1:
			missing = "end of song"
		else:
			missing = "end of verse"

		print("ERROR: Incomplete latex, " + missing + " missing")
		return None

# Write markdown song
def to_md(code, song):
	try:
		# Add title and code lines
		lines = [ "## " + song['title'] ]
		lines += [ ("#" * 5) + " " + code ]

		# Add subtitle if present
		subtitle = song["subtitle"]

		if subtitle != "":
			lines += [ f"- {subtitle}" ]
			lines += [""]

		# Generate verses
		for verse in song["verses"]:
			v_arr = []

			for line in verse:
				l_arr = []

				for seq in line:
					chars = seq["v"]

					if "i" in seq["s"]:
						chars = f"_{chars}_"

					if "b" in seq["s"]:
						chars = f"**{chars}**"

					l_arr += [ chars ]

				v_arr += [ "".join(l_arr) ]

			lines += v_arr + [""]
	except:
		print("ERROR: Invalid song with code '" + code + "'")
		return None

	# Return lines with added suffix
	return [ l + "  \n" for l in lines ]

# Write latex song
def to_latex(code, song):
	lines = []

	try:
		# Add subtitle if present
		subtitle = song.get("subtitle")

		if subtitle:
			lines += [ f"\\sing{{{subtitle}}}" ]

		# Generate verses
		for verse in song["verses"]:
			v_arr = []

			for line in verse:
				l_arr = []

				for seq in line:
					chars = seq["v"]

					if "i" in seq["s"]:
						chars = f"\\textit{{{chars}}}"

					if "b" in seq["s"]:
						chars = f"\\textbf{{{chars}}}"

					l_arr += [chars]

				v_arr += ["".join(l_arr)]

			lines += [ "\\verse{%" ] + [ "\t" + v + "\\\\%" for v in v_arr ] + ["}"]

		# Tabulate all inner lines
		lines = [ "\t" + line for line in lines ]

		# Add opening and closing lines
		newline = f"{code} = {song['title']} = {{%"
		lines = [ newline ] + lines + ["}"]
	except:
		import pprint
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(song)

		print("ERROR: Invalid song with code '" + code + "'")
		return None

	# Append each open line with a comment sign
	for l in lines:
		if l != "" and l[-1] != "}":
			l += "%"

	# Return lines with added suffix
	return [ l + "\n" for l in lines ]

# Parse markdown song file
def parse_md(fn, lines):
	language = None
	songs = {}

	if lines[0][:2] == "# ":
		language = lines[0].strip().split("in ")[-1]

	ids = [i for l, i in zip(lines, range(len(lines))) if l[:3] == "## "]
	end = len(lines)

	for i in ids[::-1]:
		code, song = from_md(lines[i:end])

		if songs.get(code):
			print("ERROR: Duplicate song code '" + code + "' in " + fn)

		songs[code] = song
		end = i

	return language, songs

def generate_song_file(path):
	filenames = [e for e in os.listdir(path) if e[-3:] == ".md"]
	song_sets = {}

	for fn in filenames:

		with open(os.path.join(path, fn), "r") as f:
			lines = f.readlines()
			language, songs = parse_md(fn, lines)
			key = fn.split(".md")[0]

			print("Processing " + lines[0][2:-1])

			song_sets[key] = {
				"language": language,
				"songs": songs,
			}

	with open("songs.dat", "w") as f:
		for key in song_sets.keys():
			song_set = song_sets[key]["songs"]

			for code in song_set.keys():
				song = song_set[code]

				f.writelines(to_latex(key + "_" + code, song))
				f.write("\n")
