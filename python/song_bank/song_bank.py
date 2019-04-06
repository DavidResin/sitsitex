import os, re

path = "input/"
filenames = os.listdir(path)
patterns = [(sym * i, t) for sym in ["\*", "_"] for i, t in zip([2,1], ['bf', 'it'])]
latex = ""

# Iterate on input files
for n in filenames:
	titles, texts = {}, {}

	# Get filename and read if valid, otherwise skip
	if n[-3:] == ".md":
		with open(path + n, "r") as f:
			data = [line.replace("\n", "").strip() for line in f.readlines()]
	else:
		continue

	# Find code
	code_ids = [idx for elem, idx in zip(data, range(len(data))) if "##### " in elem]

	# First end index is EOF
	o_idx = len(data) + 1

	# Gather songs and titles in dicts
	for idx in code_ids[::-1]:
		key = data[idx].strip().split(" ")[-1]
		titles[key] = data[idx - 1].replace("#", "").strip()
		texts[key] = data[idx + 1:o_idx - 1]
		o_idx = idx

	# Convert song text to LaTeX
	for k, v in titles.items():
		# Future : add comments, can be disabled with param in sh

		content, extra = '', ''
		in_verse = False

		# Iterate on lines
		for line in texts[k]:

			# Beginning of verse
			if not in_verse and line != '' and line[0:2] != "- ":
				in_verse = True
				content += "\t\\verse{%\n"

			# Subtitle
			if len(line) > 2 and line[:2] == "- ":
				content += "\t\\sing{" + line[2:] + "}\n"
			# End of verse
			elif in_verse and line == '':
				in_verse = False
				content += "\t}\n"
			# Comment
			#elif len(line) > 2 and line[:2] == "> ":
			#	content += "\t\\comment{" + line[2:] + "}\n"
			# Regular line
			elif line != '':
				loop = True
				mod = line

				# Loop and convert until no bold or italic text is left, then add to the text
				while loop:
					for p, t in patterns:
						pat = "^(?P<before>.*){sym}(?P<snippet>.+){sym}(?P<after>.*)$".format(sym=p)
						match = re.match(pat, mod)
						loop = bool(match)

						# Detection of pattern
						if loop:
							seg = match.groupdict()
							mod = seg['before'] + "\\text" + t + "{" + seg['snippet'] + "}" + seg['after']
							break

				content += "\t\t" + mod + "\\\\%\n"

		if in_verse:
			extra = "\t}\n"

		# Add converted song to the text
		latex += k + " = " + v + " = {%\n" + content + extra + "}\n\n"

# Write to output
with open("output/songbook.dat", "w") as f:
	f.write(latex)