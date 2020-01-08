# Standard libraries
import copy, os, re
# For Markdown parsing
import markdown as md
# For Latex compilation
import pylatex as pl
# For accentuation removal
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
# Comments are not yet supported
# Returns a tuple containing the number of missing double spaces and the number of missing/excessive empty lines
def from_md(lines, position=0):
	# Exception handling is delegated to the calling module
	n_space, n_empty = check_song(lines, position)

	newline = True
	song = dict()
	verses = []
	empty_verse = {"lines": []}
	verse = copy.deepcopy(empty_verse)
	
	for i in range(len(lines)):
		text = "Line " + str(position + i) + ": "
		tag, content, _ = cat_line(lines[i], text)

		if tag == "empty" and not newline:
			newline = True
			verses += [verse]
			verse = copy.deepcopy(empty_verse)

		elif tag in ["title", "subtitle", "code"]:
			song[tag] = "".join([s["text"] for s in content])

		elif tag in ["meta", "text"]:
			newline = False
			line = {}
			line["type"] = tag
			line["segments"] = content
			verse["lines"] += [line]

	# If empty line was missing at the end
	if not newline:
		verses += [verse]

	song["verses"] = verses
	return song, n_space, n_empty

# Check that a song is valid
# Returns a tuple containing the number of missing double spaces and the number of missing/excessive empty lines
def check_song(lines, position=0):
	# 0 : Start
	# 1 : Title parsed
	# 2 : Subtitle parsed
	# 3 : Code parsed
	# 4 : First line break parsed

	state = 0
	newline, newline_o = False, False
	comment, comment_o = False, False
	n_space, n_empty = 0, 0

	for i in range(len(lines)):
		text = "Line " + str(position + i + 1) + ": "
		tag, _, space = cat_line(lines[i], text)

		if space:
			n_space += 1

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

			newline = tag == "empty"
			comment = tag == "comment"
				
			if newline:
				# Successive empty lines
				if newline_o:
					n_empty += 1
			else:
				# Header not followed by empty line
				if state == 3:
					n_empty += 1

			if comment:
				# Comment not preceded by empty line
				if not newline_o:
					n_empty += 1

			# Comment not followed by empty line
			if comment_o and not comment and not newline:
				n_empty += 1

			state = 4
			comment_o = comment
			newline_o = newline

	return n_space, n_empty

# Function to categorize a markdown line
def cat_line(line, text=""):
	space = len(line) < 2 or line[-2:] != "  "

	if not space:
		line = line[:-2]

	# Check for empty lines
	if not line.strip():
		return "empty", None, space

	# Check for illegal characters
	if "<" in line:
		raise SyntaxError(text + "The character '<' is forbidden.")

	# Check first tag to categorize
	pat = "<(?P<tag>\w+)>"
	parsed = md.markdown(line).replace("\n", "")
	tag = match.get(re.findall(pat, parsed)[0])

	# If tag not in validation list or asterisks persist the line is invalid
	if not tag or "*" in parsed or "_ " in parsed or " _" in parsed:
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

			entry["style"] = ("b" if bold else "") + ("i" if italic else "")
			entry["text"] = e

			segments.append(entry)

	return tag, segments, space

# Write markdown song
def to_md(code, song):	
	try:
		# Add title and code lines
		lines = [ "## " + song['title'] ]

		# Add subtitle if present
		subtitle = song.get("subtitle")

		if subtitle:
			lines += [ ("#" * 4) + f" {subtitle}" ]

		lines += [ ("#" * 6) + " " + song["code"] ]

		lines += [""]

		# Generate verses
		for verse in song["verses"]:
			v_arr = []

			for line in verse["lines"]:
				l_arr = [] if line["type"] == "text" else ["> "]

				for seg in line["segments"]:
					chars = seg["text"]

					if "i" in seg["style"]:
						chars = f"_{chars}_"

					if "b" in seg["style"]:
						chars = f"**{chars}**"

					l_arr += [ chars ]

				v_arr += [ "".join(l_arr) ]

			lines += v_arr + [""]
	except:
		print(f"\tERROR: Invalid song with code '{ code }'")
		return [], True

	# Return lines with added suffix
	return [ l + "  \n" for l in lines ], False

# Write latex song
def to_latex(code, song):
	lines = []

	try:
		# Generate verses
		for verse in song["verses"]:
			v_arr = []

			for line in verse["lines"]:
				l_arr = []

				for seg in line["segments"]:
					chars = seg["text"]

					if "i" in seg["style"]:
						chars = f"\\textit{{{chars}}}"

					if "b" in seg["style"]:
						chars = f"\\textbf{{{chars}}}"

					l_arr += [chars]

				if line["type"] == "meta":
					l_arr = ["\\colorbox{gray!30}{\\sc "] + \
						l_arr + \
						["}"]

				v_arr += ["".join(l_arr)]

			lines += [ "\\verse{%" ] + [ "\t" + v + "\\\\%" for v in v_arr] + ["}"]

		# Tabulate all inner lines
		lines = [ "\t" + line for line in lines ]

		# Add opening and closing lines
		title = song['title']
		subtitle = song.get("subtitle") or "?"
		newline = f"{code} = {title} = {subtitle} = {{%"
		lines = [ newline ] + lines + ["}"]
	except:
		print(f"\tERROR: Invalid song with code '{ code }'")
		return None

	# Append each open line with a comment sign
	for l in lines:
		if l != "" and l[-1] != "}":
			l += "%"

	# Return lines with added suffix
	return [ l + "\n" for l in lines ]

# Parse markdown song file
def read_md_file(fn, lines):
	lang = "unknown language"
	songs = {}
	flag = False
	n_space, n_empty = 0, 0

	if lines[0][:2] == "# ":
		lang = lines[0].strip().split("in ")[-1]

	end = len(lines)
	ids = [i for l, i in zip(lines, range(end)) if l[:3] == "## "]
	cpls = zip(ids, ids[1:] + [end])
	str_buffer = [""]

	for c, (i, j) in enumerate(cpls, start=1):
		print(f"\rProcessing { c } song{ 's' if c != 1 else '' } from { fn } ({ lang }) ", end='')
		
		try:
			song, n_s, n_e = from_md(lines[i:j], position=i)
			code = song.get("code")
			n_space += n_s
			n_empty += n_e

			if not code:
				str_buffer += [f"\tInvalid song located at lines { i } to { j }"]
				continue

			if songs.get(code):
				raise SyntaxError(f"Duplicate song code '{ code }'")

			songs[code] = song
		except SyntaxError as err:
			str_buffer += [f"\tCritical error in { f } :"]
			str_buffer += [f"\t\t{ err_msg }"]
			flag = True

	print("\n".join(str_buffer))

	if n_space:
		print(f"\tFound and fixed { n_space } missing double ending spaces.")

	if n_empty:
		print(f"\tFound and fixed { n_empty } missing/excessive empty line(s).")

	opener = lines[0:ids[0]]

	return lang, songs, opener, flag

def generate_song_file(path_in, path_out, reg_fn, path_reg=""):
	filenames = sorted([e for e in os.listdir(path_in) if e[-3:] == ".md"])
	song_sets = {}
	language, songs, opener, flag = None, None, None, None

	for fn in filenames:
		with open(os.path.join(path_in, fn), "r", encoding="utf8") as f:
			lines = f.read().splitlines()
			language, songs, opener, flag = read_md_file(fn, lines)
			key = fn.split(".md")[0]

			song_sets[key] = {
				"language": language,
				"songs": songs,
			}

		# Correct missing spaces in the file unless an error arises.
		if flag:
			print(f"\tFile { fn } presented critical errors. It will not be autocorrected to prevent loss of data.")
		else:
			flag = False
			lines = [o.strip() + "  \n" for o in opener]

			for k in songs.keys():
				new_lines, new_flag = to_md(k, songs[k])
				lines += new_lines
				flag |= new_flag

			if flag:
				print(f'\tMarkdown compilation failed for song with code { k } in file { fn }. This should not happen. Autocorrection aborted.')
			else:
				with open(os.path.join(path_in, fn), "w", encoding="utf8") as f:
					f.writelines(lines)

	with open(os.path.join(path_out, "songs.dat"), "w", encoding="utf8") as f:
		for key in song_sets.keys():
			song_set = song_sets[key]["songs"]

			for code in song_set.keys():
				song = song_set[code]

				f.writelines(to_latex(key + "_" + code, song))
				f.write("\n")

	make_registry(path=reg_path, data=song_sets, fn=reg_fn)

# Pretty prints titles with suffixes for the song reference document
def song_suffix(key, title):
	sep = " -"
	ver = "Version"

	if '_' in key:
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

# Creates reference file for songs, sorted by language
def make_registry(path, data, fn, sort=True):
	doc = pl.Document(default_filepath=fn, \
						document_options=[ "a4paper", "twocolumn" ], \
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
			for k, s in sorted(songs.items(), key=lambda item: no_accents(item[1]['title'])):

				# Prevent separation of title and code
				with doc.create(pl.MiniPage(width=r"\textwidth")):
					doc.append(pl.HorizontalSpace("1em"))
					doc.append(s['title'])
					doc.append(pl.NewLine())
					doc.append(pl.HorizontalSpace("2em"))
					doc.append(pl.FootnoteText(pl.utils.bold(code + "_" + k)))
				
				# Space out entries
				doc.append(pl.NewLine())
				doc.append(pl.VerticalSpace(".5em"))
				doc.append(pl.NewLine())

	# Generate file
	doc.generate_pdf(filepath=path, compiler='pdflatex', clean=True)