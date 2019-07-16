import unittest
import song_helpers as module

class TestHelpers(unittest.TestCase):
	def setUp(self):
		# Define correct lines
		self.title = "## TITLE  "
		self.subtitle = "#### SUBTITLE  "
		self.code = "###### CODE  "
		self.empty = "  "
		self.comment = "    COMMENT  "
		self.meta = "> META  "
		self.text = "TEXT *ITALIC* _ITALIC_ **BOLD** __BOLD__ ***ALL*** ___ALL___  "

	def test_tagging(self):
		self.assertEqual("title", 		module.cat_line(self.title)[0])
		self.assertEqual("subtitle", 	module.cat_line(self.subtitle)[0])
		self.assertEqual("code", 		module.cat_line(self.code)[0])
		self.assertEqual("empty", 		module.cat_line(self.empty)[0])
		self.assertEqual("comment", 	module.cat_line(self.comment)[0])
		self.assertEqual("meta", 		module.cat_line(self.meta)[0])
		self.assertEqual("text", 		module.cat_line(self.text)[0])

	def test_double_space(self):
		self.assertFalse(module.cat_line(self.text)[2])
		self.assertTrue(module.cat_line("TEXTTEXT")[2])

	def test_angle_bracket(self):
		self.assertRaises(SyntaxError, module.cat_line, "<")

	def test_no_tag(self):
		self.assertRaises(SyntaxError, module.cat_line, "# FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "### FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "##### FAKE")
		self.assertRaises(SyntaxError, module.cat_line, "- FAKE")

	def test_asterisk(self):
		self.assertRaises(SyntaxError, module.cat_line, "*")
		self.assertRaises(SyntaxError, module.cat_line, "_")

	def test_duplicate_titles(self):
		song = [self.title, self.title]
		self.assertRaises(SyntaxError, module.check_song, song)

	def test_duplicate_codes(self):
		song = [self.title, self.code, self.code]
		self.assertRaises(SyntaxError, module.check_song, song)

	def test_missing_title(self):
		song = [self.code]
		self.assertRaises(SyntaxError, module.check_song, song)
		
		song = [self.subtitle]
		self.assertRaises(SyntaxError, module.check_song, song)

	def test_late_subtitle(self):
		song = [self.code, self.subtitle]
		self.assertRaises(SyntaxError, module.check_song, song)

	def test_broken_header(self):
		song = [self.empty]
		self.assertRaises(SyntaxError, module.check_song, song)

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

	def test_parsing(self):
		song = [self.title, \
				self.subtitle, \
				self.code, \
				self.empty, \
				self.comment, \
				self.empty, \
				self.meta, \
				self.text, \
				self.empty]

		data = module.from_md(song)
		
		self.assertEqual(data["title"][0]["v"], "TITLE")
		self.assertEqual(data["subtitle"][0]["v"], "SUBTITLE")
		self.assertEqual(data["code"][0]["v"], "CODE")
		self.assertEqual(data["verses"][0]["lines"][0]["type"], "meta")
		self.assertEqual(data["verses"][0]["lines"][0]["segments"][0]["v"], "META")
		self.assertEqual(data["verses"][0]["lines"][1]["type"], "text")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][0]["s"], "")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][0]["v"], "TEXT ")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][1]["s"], "i")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][1]["v"], "ITALIC")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][3]["s"], "i")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][3]["v"], "ITALIC")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][5]["s"], "b")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][5]["v"], "BOLD")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][7]["s"], "b")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][7]["v"], "BOLD")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][9]["s"], "bi")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][9]["v"], "ALL")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][11]["s"], "bi")
		self.assertEqual(data["verses"][0]["lines"][1]["segments"][11]["v"], "ALL")

if __name__ == '__main__':
	unittest.main()