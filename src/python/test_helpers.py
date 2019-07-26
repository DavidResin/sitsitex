import unittest
import song_helpers as module

class TestHelpers(unittest.TestCase):
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
		self.assertEqual("title", 		module.cat_line(self.title)[0])
		self.assertEqual("subtitle", 	module.cat_line(self.subtitle)[0])
		self.assertEqual("code", 		module.cat_line(self.code)[0])
		self.assertEqual("empty", 		module.cat_line(self.empty)[0])
		self.assertEqual("comment", 	module.cat_line(self.comment)[0])
		self.assertEqual("meta", 		module.cat_line(self.meta)[0])
		self.assertEqual("text", 		module.cat_line(self.text)[0])

	# Test that double spaced line endings are correctly detected
	def test_double_space(self):
		self.assertFalse(module.cat_line(self.text)[2])
		self.assertTrue(module.cat_line("TEXTTEXT")[2])

	# Test that the text does not contain "<"
	def test_angle_bracket(self):
		self.assertRaises(SyntaxError, module.cat_line, "<")

	# Test tags that should not be accepted
	def test_no_tag(self):
		self.assertRaises(SyntaxError, module.cat_line, "# FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "### FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "##### FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "- FAKE")

	# Test that incorrect number of styling characters is detected
	def test_asterisk(self):
		self.assertRaises(SyntaxError, module.cat_line, "*")
		self.assertRaises(SyntaxError, module.cat_line, "a _")
		self.assertRaises(SyntaxError, module.cat_line, "_ a")

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
		song = [self.code]
		self.assertRaises(SyntaxError, module.check_song, song)
		
		song = [self.subtitle]
		self.assertRaises(SyntaxError, module.check_song, song)

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
		# Double empty lines
		song = [self.title, self.code, self.empty, self.empty]
		self.assertTrue(module.check_song(song))

		# Missing empty line after header
		song = [self.title, self.code, self.text]
		self.assertTrue(module.check_song(song))

		# Missing empty line before comment
		song = [self.title, self.code, self.empty, self.text, self.comment]
		self.assertTrue(module.check_song(song))

		# Missing empty line after comment
		song = [self.title, self.code, self.empty, self.comment, self.text]
		self.assertTrue(module.check_song(song))

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

		self.assertFalse(module.check_song(song))

	# Test parsing of verses
	def test_verse_parsing(self):
		song = [self.title, \
				self.code, \
				self.empty, \
				self.text, \
				self.empty, \
				self.text2, \
				self.empty]

		processed, _ = module.to_md("", module.from_md(song))

		self.assertEqual(len(song), len(processed))

		for s, p in zip(song, processed):
			self.assertEqual(s.replace("*", "_"), p.replace("*", "_").replace("\n", ""))

	# Test parsing of styling characters
	def test_style_parsing(self):
		song = [self.title, \
				self.subtitle, \
				self.code, \
				self.empty, \
				self.meta, \
				self.text]

		data = module.from_md(song)
		
		self.assertEqual(data["title"], "TITLE")
		self.assertEqual(data["subtitle"], "SUBTITLE")
		self.assertEqual(data["code"], "CODE")
		self.assertEqual(data["verses"][0]["lines"][0]["type"], "meta")
		self.assertEqual(data["verses"][0]["lines"][0]["segments"][0]["text"], "META")
		self.assertEqual(data["verses"][0]["lines"][1]["type"], "text")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][0]["style"], "")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][0]["text"], "TEXT ")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][1]["style"], "i")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][1]["text"], "ITALIC")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][3]["style"], "i")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][3]["text"], "ITALIC")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][5]["style"], "b")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][5]["text"], "BOLD")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][7]["style"], "b")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][7]["text"], "BOLD")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][9]["style"], "bi")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][9]["text"], "ALL")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][11]["style"], "bi")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][11]["text"], "ALL")

if __name__ == '__main__':
	unittest.main()