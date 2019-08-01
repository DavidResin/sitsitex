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
	"blockquote": "note",
	"p": "line",
}

def verify_song(cat_lines):
	for tag, data in cat_lines:
		

def cat_line(raw_line):
	line = raw_line.strip()

	# Check for empty lines
	if not line:
		return line, "empty"

	# Check for illegal characters
	if "<" in line or ">" in line:
		raise Exception("Characters '<' and '>' are forbidden.")

	# Check first tag to categorize
	pat = "^<(?P<tag>.+)>.+$"
	parsed = md.markdown(line)
	tag = match.get(re.match(pat, parsed).groupdict()["tag"])

	# If tag not in validation list the line is invalid
	if not tag:
		raise Exception("Invalid markdown.")

	# remove all tags except those in keep with or without /

	keep_str = "|".join(keep)
	i = 0
	segs = []
	bf, it = False, False
	style = ""
	text = ""

	while i < len(parsed):
		# Any tag detected
		g_lkp = re.search(r'<.*?>', parsed[i:])
		# Style tag detected
		k_lkp = re.search(r'</?(' + keep_str + ')>', parsed[i:])

		if g_lkp:
			start, end = g_lkp.span()
			text += parsed[i:start]
			i = end

			if k_lkp:
				bf = bf ^ "strong" in k_lkp.group()
				it = it ^ "em" in k_lkp.group()
			else:
				# Ignore other tags
				continue
		else:
			# If no more tags
			text += parsed[i:]

		segs += [{
			"style": style,
			"text": text
		}]

		text = ""
		style = "b" * bf + "i" * it