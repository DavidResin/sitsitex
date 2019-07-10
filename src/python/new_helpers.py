import markdown as md
import re

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