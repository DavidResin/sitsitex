import re
import markdown as md

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
			elif len(l) > 2 and l[:2] == "# ":
				song["title"] = l[2:]
				state = 1
			else:
				invalid = True

		# Parse code
		elif state == 1:
			if l == "":
				print("WARNING: Useless empty line in markdown")
			elif len(l) > 6 and l[:6] == "##### ":
				song["code"] = l[6:]
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
			return None

	if state == 4:
		return song
	else:
		if state == 0:
			missing = "title"
		elif state == 1:
			missing = "code"
		else:
			missing = "verse(s)"

		print("ERROR: Incomplete markdown, " + missing + " missing")
		return None

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
				song["code"] = seg["code"]
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
		return song
	else:
		if state == 0:
			missing = "title and code"
		elif state == 1:
			missing = "end of song"
		else:
			missing = "end of verse"

		print("ERROR: Incomplete latex, " + missing + " missing")
		return None

def to_md(song):
	try:
		# Add title and code lines
		lines = [ "# " + song['title'] ]
		lines += [ ("#" * 5) + " " + song['code'] ]

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
		print("ERROR: Invalid song")
		return None

	# Return lines with added suffix
	return [ l + "  \n" for l in lines ]

def to_latex(song):
	try:
		# Add subtitle if present
		subtitle = song["subtitle"]

		if subtitle != "":
			lines = [ f"\\sing{{{subtitle}}}" ]

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

			lines += [ "\\verse{" ] + [ "\t" + v + "\\\\" for v in v_arr ] + ["}"]

		# Tabulate all inner lines
		lines = [ "\t" + line for line in lines ]

		# Add opening and closing lines
		newline = f"{song['code']} = {song['title']} = {{"
		lines = [ newline ] + lines + ["}"]
	except:
		print("ERROR: Invalid song")
		return None

	# Append each open line with a comment sign
	for l in lines:
		if l != "" and l[-1] != "}":
			l += "%"

	# Return lines with added suffix
	return [ l + "\n" for l in lines ]

song = {
	"title": "TITLE",
	"subtitle": "SUB",
	"code": "CODE",
	"verses": [
		[
			[
				{
					"v": "(Solo:)",
					"s": "i",
				},
			],
		],
	],
}