# This file's sole purpose is to convert the data from the old
# .dat TeX format into markdown for ease of reading.

# Regexp library
import re

# Read input file
input_f = open("songbook.dat", "r")
lines = input_f.readlines()
input_f.close()

# Replacement dicts
map_1 = {
	'\n': '',
	'\t': '',
	'\\\\': '',
	'%': '',
	'\\solo': '_(Songmaster solo:)_',
	'\\everyone': '_(Everyone:)_',
	'\\sing{Solo:}': '_(Solo:)_',
	'\\sing{All:}': '_(All:)_',
}

map_2 = {
	'\\twice{': '',
	'}': '',
}

map_3 = {
	'\\verse{': '',
}

# 1st stage of auto-replace
for k, v in map_1.items():
	lines = [s.replace(k, v) for s in lines]

# Complex replacements
id_open, id_close = 0, 0
twice = False

for l, idx in zip(lines, range(len(lines))):

	# Titles
	match = re.match(r"^(?P<code>.+) = (?P<name>.+) = {$", l)

	if bool(match):
		data = match.groupdict()
		lines[idx] = "\n# " + data["name"] + "\n##### " + data["code"]

	# Subtitles
	elif '\\tuneof{' in l:
		lines[idx] = '- _To the tune of “' + l.split('\\tuneof{')[1] + '”_'
	elif '\\tuneof[' in l:
		cut1 = l.split(']{')
		cut2 = cut1[0].split('\\tuneof[')
		lines[idx] = '- _To the tune of “' + cut1[1] + '”, ' + cut2[1] + '_'

	# Directions
	elif '\\sing{' in l:
		lines[idx] = '_' + l.split('\\sing{')[1] + '_'

	# Bold text
	elif '\\textbf{' in l:
		cut1 = l.split('\\textbf{')
		cut2 = cut1[1].split('}')
		lines[idx] = cut1[0] + '**' + cut2[0] + '**' + cut2[1]

	# Repetitions
	elif '\\twice{' in l:
		twice = True
		id_open = idx + 1
	elif twice and '}' in l:
		twice = False
		id_close = idx - 1
		lines[id_open] = ":;: " + lines[id_open]
		lines[id_close] = lines[id_close] + " :;:"

# 2nd stage of auto-replace
for k, v in map_2.items():
	lines = [s.replace(k, v) for s in lines]

# Remove empty lines
lines = [l for l in lines if l != '']

# 3rd stage of auto-replace
for k, v in map_3.items():
	lines = [s.replace(k, v) for s in lines]

# Write to file
output_f = open("song_data.md", "w")

# We add 2 spaces at the end of each line to force a line break in markdown readers
for l in lines:
	output_f.write(l + "  \n")

output_f.close()