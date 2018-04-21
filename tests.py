import unittest
from transformparse import TransformParser
import xml.etree.ElementTree as ElementTree

class TestTransformParse(unittest.TestCase):

	def test_instruction_string_single(self):
		test_input = '[rename, /memory[1]/mailbox[1], box]'
		expected_output = ['[rename, /memory[1]/mailbox[1], box]']
		parser = TransformParser(test_input)
		elems = parser._get_instruction_strings()
		self.assertEqual(elems, expected_output)

	def test_instruction_string_multiple(self):
		test_input = '[rename, /memory[1]/mailbox[1], box][rename, /memory[1]/mailbox[1], box]'
		expected_output = ['[rename, /memory[1]/mailbox[1], box]', '[rename, /memory[1]/mailbox[1], box]']
		parser = TransformParser(test_input)
		elems = parser._get_instruction_strings()
		self.assertEqual(elems, expected_output)

	def test_instruction_string_none(self):
		test_input = ''
		expected_output = []
		parser = TransformParser(test_input)
		elems = parser._get_instruction_strings()
		self.assertEqual(elems, expected_output)

	def test_instruction_string_invalid(self):
		test_input = '[rename, /memory[1]/mailbox[1], box'
		expected_output = []
		parser = TransformParser(test_input)
		elems = parser._get_instruction_strings()
		self.assertEqual(elems, expected_output)


class TestTransformInstructions(unittest.TestCase):

	maxDiff = 1000

	test_rename_xml_input = '<memory> <mailbox path="/var/spool/mail/almaster"/> </memory>'
	test_rename_transform_input = '[rename, /memory[1]/mailbox[1], box]'
	test_rename_expected_output = '<memory> <box path="/var/spool/mail/almaster"/> </memory>'

	test_update_xml_input = '<memory> <mailbox path="/var/spool/mail/almaster"/> </memory>'
	test_update_transform_input = '[update, /memory[1]/mailbox[1]/@path, /new/path/]'
	test_update_expected_output = '<memory> <mailbox path="/new/path/"/> </memory>'

	test_append_first_xml_input = '<oopoyy><function/></oopoyy>'
	test_append_first_transform_input = '[append-first, /oopoyy[1], <gap/>]'
	test_append_first_expected_output = '<oopoyy><gap/><function/></oopoyy>'

	test_append_xml_input = '<oopoyy><function/></oopoyy>'
	test_append_transform_input = '[append, /oopoyy[1], <gap/>]'
	test_append_expected_output = '<oopoyy><function/><gap/></oopoyy>'

	test_insert_after_xml_input = '<Tests><Test type="Add element"><One>1</One><One>2</One><One>2.1</One><One>3</One></Test><Test type="Delete element"><Two>1</Two><Two>3</Two></Test><Test type="Move element"><Three>2</Three><Three>1</Three><Three>3</Three></Test></Tests>'
	test_insert_after_transform_input = '[insert-after, /Tests[1]/Test[2],<Test><Seven>This is the third sentence.</Seven></Test>]'
	test_insert_after_expected_output = '<Tests><Test type="Add element"><One>1</One><One>2</One><One>2.1</One><One>3</One></Test><Test type="Delete element"><Two>1</Two><Two>3</Two></Test><Test><Seven>This is the third sentence.</Seven></Test><Test type="Move element"><Three>2</Three><Three>1</Three><Three>3</Three></Test></Tests>'

	test_move_first_xml_input = '<a><b></b><c></c></a>'
	test_move_first_transform_input = '[move-first, /a[1]/c[1], /a[1]]'
	test_move_first_expected_output = '<a><c></c><b></b></a>'

	test_move_after_xml_input = '<a><b></b><c></c></a>'
	test_move_after_transform_input = '[move-after, /a[1]/b[1], /a[1]/c[1]]'
	test_move_after_expected_output = '<a><c></c><b></b></a>'

	test_remove_xml_input = '<a><b></b><c></c></a>'
	test_remove_transform_input = '[remove, /a[1]/b[1]]'
	test_remove_expected_output = '<a><c></c></a>'

	def _transform_test(self, xml_input, transform_input, xml_output):
		parser = TransformParser(transform_input)
		instructions = parser.parse()
		output = parser.apply(instructions, xml_input)
		# Normalise expected
		ex_root = ElementTree.fromstring(xml_output)
		expected = ElementTree.tostring(ex_root, encoding="unicode")

		self.assertEqual(output, expected)

	def test_rename(self):
		self._transform_test(self.test_rename_xml_input, self.test_rename_transform_input, self.test_rename_expected_output)

	def test_update(self):
		self._transform_test(self.test_update_xml_input, self.test_update_transform_input, self.test_update_expected_output)

	def test_append_first(self):
		self._transform_test(self.test_append_first_xml_input, self.test_append_first_transform_input, self.test_append_first_expected_output)

	def test_append(self):
		self._transform_test(self.test_append_xml_input, self.test_append_transform_input, self.test_append_expected_output)

	def test_insert_after(self):
		self._transform_test(self.test_insert_after_xml_input, self.test_insert_after_transform_input, self.test_insert_after_expected_output)

	def test_move_first(self):
		self._transform_test(self.test_move_first_xml_input, self.test_move_first_transform_input, self.test_move_first_expected_output)

	def test_move_after(self):
		self._transform_test(self.test_move_after_xml_input, self.test_move_after_transform_input, self.test_move_after_expected_output)

	def test_remove(self):
		self._transform_test(self.test_remove_xml_input, self.test_remove_transform_input, self.test_remove_expected_output)

if __name__ == '__main__':
	unittest.main()