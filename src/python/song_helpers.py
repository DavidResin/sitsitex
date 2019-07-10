import os, re
import markdown as md
import pylatex as pl
import unicodedata as ud

# tags to keep
keep = ["em", "strong"]

# Categories of lines depending on the opening tag
match = {
	"h2": "title",
	"h4": "subtitle",
	"h6": "code",
	"pre": "comment",
	"code": "comment",
	"blockquote": "meta",
	"p": "text",
}

# Parse Markdown song
def parse_md(lines, position=0):
	# Exception handling is delegated to the calling module
	check_song(lines, position)

	newline = False
	song = dict()
	verses = []
	empty_verse = {"lines": []}
	verse = empty_verse.copy()
	
	for i in range(len(lines)):
		text = "Line " + str(position + i) + ": "
		tag, content = cat_line(lines[i], text)

		if tag in ["title", "subtitle", "code"]:
			song[tag] = content

		elif tag == "empty" and not newline:
			newline = True
			verses += [verse]
			verse = empty_verse.copy()

		elif tag in ["meta", "text"]:
			line = {}
			line["type"] = tag
			line["segments"] = content
			verse += [line]

	# If empty line was missing at the end
	if not newline:
		verses += [verse]

	song["verses"] = verses

# Check that a song is valid, return value is for minor syntax problems
def check_song(lines, position=0):
	# 0 : Start
	# 1 : Title parsed
	# 2 : Subtitle parsed
	# 3 : Code parsed
	# 4 : First line break parsed
	state = 0
	newline, newline_o = False, False
	comment, comment_o = False, False
	ret = False

	for i in range(len(lines)):
		text = "Line " + str(position + i) + ": "
		tag, _, space = cat_line(lines[i], text)

		if space:
			print(text + "should end with a double space.")

		if tag == "title":
			if state > 0:
				raise SyntaxError(text + "Cannot have more than one title.")

			state = 1

		elif tag == "subtitle":
			if state < 1:
				raise SyntaxError(text + "Title missing.")
			elif state > 1:
				raise SyntaxError(text + "Subtitle misplaced, possible duplicate.")

			state = 2

		elif tag == "code":
			if state < 1:
				raise SyntaxError(text + "Title missing.")
			elif state > 2:
				raise SyntaxError(text + "Cannot have more than one code.")

			state = 3

		else:
			if state < 3:
				raise SyntaxError(text + "Invalid header.")
				
			if tag == "empty":
				if newline_o:
					print(text + "Successive empty lines are useless.")
					ret = True

				newline = True

				if state == 3:
					state = 4
			else:
				if state == 3:
					print(text + "Header should be followed by an empty line.")
					ret = True

				newline = False

			if tag == "comment":
				if not newline_o:
					print(text + "Comments should be preceded by an empty line.")
					ret = True

				comment = True
			else:
				comment = False

			if comment_o and not comment and not newline:
				print(text + "Comments should be followed by an empty line.")
				ret = True

			comment_o = comment
			newline_o = newline

	return ret

# Function to categorize a markdown line
def cat_line(line, text=""):
	space = len(line) < 2 or line[-2:] != "  "

	# Check for empty lines
	if not line.strip():
		return "empty", None, space

	# Check for illegal characters
	if "<" in line:
		raise SyntaxError(text + "The character '<' is forbidden.")

	# Check first tag to categorize
	pat = "<(?P<tag>\w+)>"
	parsed = md.markdown(line.replace("_", "*"))
	tag = match.get(re.findall(pat, parsed)[0])

	# If tag not in validation list or asterisks persist the line is invalid
	if not tag or "*" in parsed:
		raise SyntaxError(text + "Invalid markdown.")

	# Remove all tags except those in keep with or without /
	keep_str = "|".join(keep)
	proc = parsed
	elems = []

	while proc:
		# Scans for all tags
		g_lkp = re.search(r'<.*?>', proc)
		# Scans only for style tags
		k_lkp = re.search(r'</?(' + keep_str + ')>', proc)

		if g_lkp:
			s0, s1 = g_lkp.span()

			# If text before tag, remember it
			if s0:
				elems += [proc[:s0]]

			# If next tag is a style tag, remember it
			if k_lkp and k_lkp.span() == g_lkp.span():
				elems += [proc[s0:s1]]

			# Remove processed text
			proc = proc[s1:]

		# If no more tags left, just remember the remander
		else:
			elems += [proc]
			break

	# Parse cleaned line
	bold, italic = False, False
	segments = []

	for e in elems:
		if "<" in e:
			if "strong" in e:
				bold = not bold
			if "em" in e:
				italic = not italic
		else:
			entry = {}

			entry["s"] = ("b" if bold else "") + ("i" if italic else "")
			entry["v"] = e

			segments.append(entry)

	return tag, segments, space

# Read latex song (DO NOT USE)
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
			return None, None

		if invalid:
			print("ERROR: Invalid latex, please check the style guide")
			print("Line: " + l)
			print("State: " + str(state))
			return None, None

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
		return None, None

# Write markdown song
def to_md(code, song):
	#print("UNSAFE FOR NOW")
	#return
	
	try:
		# Add title and code lines
		lines = [ "## " + song['title'] ]

		# Add subtitle if present
		subtitle = song.get("subtitle")

		#if subtitle:
		#	lines += [ ("#" * 4) + f" {subtitle}" ]

		lines += [ ("#" * 5) + " Code: " + code ]



		if subtitle:
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
		print("ERROR: Invalid song with code '" + code + "'")
		return None

	# Append each open line with a comment sign
	for l in lines:
		if l != "" and l[-1] != "}":
			l += "%"

	# Return lines with added suffix
	return [ l + "\n" for l in lines ]

# Parse markdown song file
def read_md_file(fn, lines):
	language = "unknown language"
	songs = {}

	if lines[0][:2] == "# ":
		language = lines[0].strip().split("in ")[-1]

	print("Processing songs from file", fn, "in", language)

	end = len(lines)
	ids = [i for l, i in zip(lines, range(end)) if l[:3] == "## "]
	cpls = zip(ids, ids[1:] + [end])

	for i, j in cpls:
		code, song = from_md(lines[i:j])

		if not code:
			print("Invalid song located at lines", i, "to", end)
			continue

		if songs.get(code):
			print("ERROR: Duplicate song code '" + code + "' in " + fn)
			continue

		songs[code] = song

	opener = lines[0:ids[0]]

	return language, songs, opener

def generate_song_file(path, reg_fn, reg_path=""):
	filenames = sorted([e for e in os.listdir(path) if e[-3:] == ".md"])
	song_sets = {}
	language, songs, opener = None, None, None

	for fn in filenames:
		with open(os.path.join(path, fn), "r", encoding="utf8") as f:
			lines = f.read().splitlines()
			language, songs, opener = read_md_file(fn, lines)
			key = fn.split(".md")[0]

			song_sets[key] = {
				"language": language,
				"songs": songs,
			}

		# Correct missing spaces in the file
		with open(os.path.join(path, fn), "w", encoding="utf8") as f:
			lines = [o + "  \n" for o in opener]

			for k in songs.keys():
				lines += to_md(k, songs[k])

			f.writelines(lines)

	with open("songs.dat", "w", encoding="utf8") as f:
		for key in song_sets.keys():
			song_set = song_sets[key]["songs"]

			for code in song_set.keys():
				song = song_set[code]

				f.writelines(to_latex(key + "_" + code, song))
				f.write("\n")

	make_register(path=reg_path, data=song_sets, fn=reg_fn)

def song_suffix(key, title):
	if '_' in key:
		sep = " -"
		ver = "Version"
		num = ""
		det = key.split('_')[1:]

		if det[-1].isdigit():
			num = det[-1]
			det = det[:-1]

		return (title + " ".join([sep] + det + [ver, num]).title()).strip()

	return title

# Removes accents from a given string
def no_accents(input_str):
    nfkd_form = ud.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not ud.combining(c)])

def make_register(path, data, fn, sort=True):
	doc = pl.Document(default_filepath=fn, \
						document_options={ "twocolumn" }, \
						geometry_options={ "margin" : "1in" }, \
						indent=False, \
						fontenc="T1", \
						inputenc="utf8")

	# Preamble
	title = pl.utils.NoEscape(r'Sitsi\TeX{} Song Registry')
	doc.preamble.append(pl.Command('title', title))
	doc.preamble.append(pl.Command('date', ''))

	# Content
	doc.append(pl.utils.NoEscape(r'\maketitle'))

	for code, v in data.items():
		songs = v['songs']
		section = v['language'].title() + " (" + str(len(songs)) + " songs)"

		with doc.create(pl.Section(section, numbering=False)):

			# Sort songs in alphabetical order, ignoring accentuation
			for k, s in sorted(songs.items(), key=lambda item: no_accents(item[1]['entry'])):

				# Prevent separation of title and code
				with doc.create(pl.MiniPage(width=r"\textwidth")):
					doc.append(pl.HorizontalSpace("1em"))
					doc.append(s['entry'])
					doc.append(pl.NewLine())
					doc.append(pl.HorizontalSpace("2em"))
					doc.append(pl.FootnoteText(pl.utils.bold(code + "_" + k)))
				
				# Space out entries
				doc.append(pl.NewLine())
				doc.append(pl.VerticalSpace(".5em"))
				doc.append(pl.NewLine())

	# Generate file
	doc.generate_pdf(filepath=path, compiler='pdflatex', clean=True)