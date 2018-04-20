import unittest
from transformparse import TransformParser

class TestTransformInstructions(unittest.TestCase):

	test_rename_xml_input = '<memory> <mailbox path="/var/spool/mail/almaster"/> </memory>'
	test_rename_transform_input = '[rename, /memory[1]/mailbox[1], box]'
	test_rename_expected_output = '<memory> <box path="/var/spool/mail/almaster"/> <memory>'

	def test_rename(self):
		parser = TransformParser(test_rename_transform_input)
		parser.parse()
		output = parser.apply(test_rename_xml_input)
		self.assertEqual(output, test_rename_expected_output)

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