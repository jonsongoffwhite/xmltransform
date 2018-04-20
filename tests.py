import unittest
from transformparse import TransformParser

class TestTransformParse(unittest.TestCase):

	def test_parse_single(self):
		test_input = '[rename, /memory[1]/mailbox[1], box]'
		expected_output = ['[rename, /memory[1]/mailbox[1], box]']
		parser = TransformParser(test_input)
		elems = parser.parse()
		self.assertEqual(elems, expected_output)

	def test_parse_multiple(self):
		test_input = '[rename, /memory[1]/mailbox[1], box][rename, /memory[1]/mailbox[1], box]'
		expected_output = ['[rename, /memory[1]/mailbox[1], box]', '[rename, /memory[1]/mailbox[1], box]']
		parser = TransformParser(test_input)
		elems = parser.parse()
		self.assertEqual(elems, expected_output)

	def test_parse_none(self):
		pass

	def test_parse_invalid(self):
		pass


class TestTransformInstructions(unittest.TestCase):

	test_rename_xml_input = '<memory> <mailbox path="/var/spool/mail/almaster"/> </memory>'
	test_rename_transform_input = '[rename, /memory[1]/mailbox[1], box]'
	test_rename_expected_output = '<memory> <box path="/var/spool/mail/almaster"/> <memory>'

	def test_rename(self):
		parser = TransformParser(self.test_rename_transform_input)
		parser.parse()
		output = parser.apply(self.test_rename_xml_input)
		self.assertEqual(output, self.test_rename_expected_output)

	def test_update(self):
		pass

	def test_append_first(self):
		pass

	def test_append(self):
		pass

	def test_insert_after(self):
		pass

	def test_move_first(self):
		pass

	def test_move_after(self):
		pass

	def test_remove(self):
		pass

if __name__ == '__main__':
	unittest.main()