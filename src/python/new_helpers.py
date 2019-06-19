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

def cat_line(line):
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
	spans = set()
	proc = parsed

	for i in range(len(parsed)):
		g_lkp = re.search(r'<.*?>', proc)
		k_lkp = re.search(r'</?(' + keep_str + ')>', proc)
