import unittest
from scripts import parse as module

class TestParse(unittest.TestCase):
	# Setup working lines
	def setUp(self):
		# Define correct lines
		self.title = "## TITLE  "
		self.subtitle = "#### SUBTITLE  "
		self.code = "###### CODE  "
		self.empty = "  "
		self.comment = "    COMMENT  "
		self.meta = "> META  "
		self.text = "TEXT *ITALIC* _ITALIC_ **BOLD** __BOLD__ ***ALL*** ___ALL___  "
		self.text2 = "MOAR TEXT  "

	# Test that tags are recognized
	def test_tagging(self):
		data = [
			("title", self.title),
			("subtitle", self.subtitle),
			("code", self.code),
			("empty", self.empty),
			("comment", self.comment),
			("meta", self.meta),
			("text", self.text)
		]

		for i, (d1, d2) in enumerate(data):
			with self.subTest(i=i):
				self.assertEqual(d1, module.cat_line(d2)[0])

	# Test that double spaced line endings are correctly detected
	def test_double_space(self):
		with self.subTest(i=0):
			self.assertFalse(module.cat_line(self.text)[2])

		with self.subTest(i=1):
			self.assertTrue(module.cat_line("TEXTTEXT")[2])

	# Test that the text does not contain "<"
	def test_angle_bracket(self):
		self.assertRaises(SyntaxError, module.cat_line, "<")

	# Test tags that should not be accepted
	def test_no_tag(self):
		data = ["# FAKE", "### FAKE", "##### FAKE", "- FAKE"]

		for i, d in enumerate(data):
			with self.subTest(i=i):
				self.assertRaises(SyntaxError, module.cat_line, d)

	# Test that incorrect number of styling characters is detected
	def test_asterisk(self):
		data = ["*", "a _", "_ a"]

		for i, d in enumerate(data):
			with self.subTest(i=i):
				self.assertRaises(SyntaxError, module.cat_line, d)

	# Test detection of duplicate titles
	def test_duplicate_titles(self):
		song = [self.title, self.title]
		self.assertRaises(SyntaxError, module.check_song, song)

	# Test detection of duplicate codes
	def test_duplicate_codes(self):
		song = [self.title, self.code, self.code]
		self.assertRaises(SyntaxError, module.check_song, song)

	# Test detection of missing title
	def test_missing_title(self):
		data = [self.code, self.subtitle]

		for i, d in enumerate(data):
			with self.subTest(i=i):
				self.assertRaises(SyntaxError, module.check_song, [d])
	
	# Test detection of misplaced subtitle
	def test_late_subtitle(self):
		song = [self.code, self.subtitle]
		self.assertRaises(SyntaxError, module.check_song, song)

	# Test detection of invalid header
	def test_broken_header(self):
		song = [self.empty]
		self.assertRaises(SyntaxError, module.check_song, song)

	# Test detection of missing newlines
	def test_newlines(self):
		data = [
			# Double empty lines
			[self.title, self.code, self.empty, self.empty],
			# Missing empty line after header
			[self.title, self.code, self.text],
			# Missing empty line before comment
			[self.title, self.code, self.empty, self.text, self.comment],
			# Missing empty line after comment
			[self.title, self.code, self.empty, self.comment, self.text]
		]

		for i, d in enumerate(data):
			with self.subTest(i=i):
				self.assertEqual(module.check_song(d), (0, 1))

	# Test acceptance of correct song structure
	def test_correct_song(self):
		song = [self.title, \
				self.subtitle, \
				self.code, \
				self.empty, \
				self.comment, \
				self.empty, \
				self.meta, \
				self.text, \
				self.empty]

		self.assertEqual(module.check_song(song), (0, 0))

	# Test parsing of verses
	def test_verse_parsing(self):
		song = [self.title, \
				self.code, \
				self.empty, \
				self.text, \
				self.empty, \
				self.text2, \
				self.empty]

		temp, _, _ = module.from_md(song)
		processed, _ = module.to_md("", temp)

		with self.subTest(i=0):
			self.assertEqual(len(song), len(processed))

		for i, (s, p) in enumerate(zip(song, processed), 1):
			with self.subTest(i=i):
				self.assertEqual(s.replace("*", "_"), p.replace("*", "_").replace("\n", ""))

	# Test parsing of styling characters
	def test_style_parsing(self):
		song = [self.title, \
				self.subtitle, \
				self.code, \
				self.empty, \
				self.meta, \
				self.text]

		parsed, _, _ = module.from_md(song)

		data = [
			(parsed["title"], "TITLE"),
			(parsed["subtitle"], "SUBTITLE"),
			(parsed["code"], "CODE"),
			(parsed["verses"][0]["lines"][0]["segments"][0]["text"], "META")
		]

		for i, d in enumerate(["meta", "text"]):
			data += [(parsed["verses"][0]["lines"][i]["type"], d)]

		indices = [0, 1, 3, 5, 7, 9, 11]
		texts = ["TEXT ", "ITALIC", "ITALIC", "BOLD", "BOLD", "ALL", "ALL"]
		styles = ["", "i", "i", "b", "b", "bi", "bi"]
		segments = parsed["verses"][0]["lines"][1]["segments"]

		for i, t, s in zip(indices, texts, styles):
			data += [(segments[i]["text"], t)]
			data += [(segments[i]["style"], s)]

		for i, (d1, d2) in enumerate(data):
			with self.subTest(i=i):
				self.assertEqual(d1, d2)

if __name__ == '__main__':
	unittest.main()