import unittest
from transformparse import TransformParser
import xml.etree.ElementTree as ElementTree
from xml_compare import xml_compare
import logging
import sys

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

    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "TestTransformInstructions" ).setLevel( logging.DEBUG )
    log= logging.getLogger( "TestTransformInstructions" )



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

    test_move_after_xml_input = '<a><b></b><c></c><d></d><e></e><f></f></a>'
    test_move_after_transform_input = '[move-after, /a[1]/b[1], /a[1]/c[1]]'
    test_move_after_expected_output = '<a><c></c><b></b><d></d><e></e><f></f></a>'

    test_remove_xml_input = '<a><b></b><c></c></a>'
    test_remove_transform_input = '[remove, /a[1]/b[1]]'
    test_remove_expected_output = '<a><c></c></a>'

    test_remove_indexed_text_xml_input = '<a><b>Not This</b><c>Hello</c></a>'
    test_remove_indexed_text_transform_input = '[remove, /a[1]/c[1]/text()[1]]'
    test_remove_indexed_text_expected_output = '<a><b>Not This</b><c></c></a>'

    test_two_xml_input = '<oopoyy><function/></oopoyy>'
    test_two_transform_input = '[append, /oopoyy[1], <gap/>][remove, /function[1]]'
    test_two_expected_output = '<oopoyy><gap/></oopoyy>'

    test_rename_attribute_xml_input = '<memory> <mailbox path="/var/spool/mail/almaster"/> </memory>'
    test_rename_attribute_transform_input = '[rename, /memory[1]/mailbox[1]/@path, route]'
    test_rename_attribute_expected_output = '<memory> <mailbox route="/var/spool/mail/almaster"/> </memory>'

    test_update_indexed_text_xml_input = '<a><b>Hello World!<d></d>Bye World!</b><c></c></a>'
    test_update_indexed_text_transform_input = '[update, /a[1]/b[1]/text()[2], New Text!]'
    test_update_indexed_text_expected_output = '<a><b>Hello World!<d></d>New Text!</b><c></c></a>'

    #test_move_first_indexed_text_xml_input = '<a><b>Not This</b><c>Hello</c></a>'
    #test_move_first_indexed_text_transform_input = '[move-first, /a[1]/c[1]/text()[1], /a[1]]'
    #test_move_first_indexed_text_expected_output = '<a>Hello<b>Not This</b><c></c></a>'

    test_move_after_indexed_text_xml_input = '<a><b>Not This</b><c>Hello</c><d></d></a>'
    test_move_after_indexed_text_transform_input = '[move-after, /a[1]/d[1], /a[1]/b[1]/text()[1]]'
    test_move_after_indexed_text_expected_output = '<a><b>Not This<d></d></b><c>Hello</c></a>'

    oddity_0_xml_in = '<a>ii<LogilabXMLDIFFFAKETag /><b />moretext</a>'
    oddity_0_transform_in = '[move-after, /a[1]/b[1], /a[1]/text()[2]]'
    oddity_0_xml_out = '<a>ii<LogilabXMLDIFFFAKETag />moretext<b/></a>'


    def _transform_test(self, xml_input, transform_input, xml_output):
        ex_root = ElementTree.fromstring(xml_output)

        parser = TransformParser(transform_input)
        instructions = parser.parse()
        output_tree = parser.apply(instructions, xml_input)
        output_root = output_tree.getroot()
        # Normalise expected
        
        self.assertTrue(xml_compare(output_root, ex_root))

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

    def test_two(self):
        self._transform_test(self.test_two_xml_input, self.test_two_transform_input, self.test_two_expected_output)

    def test_rename_attribute(self):
        self._transform_test(self.test_rename_attribute_xml_input, self.test_rename_attribute_transform_input, self.test_rename_attribute_expected_output)

    def test_update_indexed_text(self):
        self._transform_test(self.test_update_indexed_text_xml_input, self.test_update_indexed_text_transform_input, self.test_update_indexed_text_expected_output)

    #def test_move_first_indexed_text(self):
    #    self._transform_test(self.test_move_first_indexed_text_xml_input, self.test_move_first_indexed_text_transform_input, self.test_move_first_indexed_text_expected_output)

    def test_move_after_indexed_text(self):
        pass
        self._transform_test(self.test_move_after_indexed_text_xml_input, self.test_move_after_indexed_text_transform_input, self.test_move_after_indexed_text_expected_output)

    def test_remove_indexed_text(self):
        self._transform_test(self.test_remove_indexed_text_xml_input, self.test_remove_indexed_text_transform_input, self.test_remove_indexed_text_expected_output)

    def test_oddity_0(self):
        self._transform_test(self.oddity_0_xml_in, self.oddity_0_transform_in, self.oddity_0_xml_out)



class TestMultipleTransformInstructions(unittest.TestCase):

    maxDiff = 1000

    def _file_test(self, xml_filename, transform_filename, expected_filename):
        with open(transform_filename, 'r') as transform_file:
            transform_input = transform_file.read()

        xml_input = ElementTree.parse(xml_filename)

        expected_xml_root = ElementTree.parse(expected_filename).getroot()

        parser = TransformParser(transform_input)
        instructions = parser.parse()
        output_tree = parser.apply(instructions, ElementTree.tostring(xml_input.getroot(), encoding="unicode"))

        output_root = output_tree.getroot()


        self.assertTrue(xml_compare(output_root, expected_xml_root))

    def test_00(self):
        self._file_test('tests/test_00_1.xml', 'tests/test_00_diff.result', 'tests/test_00_2.xml')

    def test_01(self):
        self._file_test('tests/test_01_1.xml', 'tests/test_01_diff.result', 'tests/test_01_2.xml')

    def test_02(self):
        self._file_test('tests/test_02_1.xml', 'tests/test_02_diff.result', 'tests/test_02_2.xml')

    def test_03(self):
        self._file_test('tests/test_03_1.xml', 'tests/test_03_diff.result', 'tests/test_03_2.xml')

    def test_04(self):
        self._file_test('tests/test_04_1.xml', 'tests/test_04_diff.result', 'tests/test_04_2.xml')


if __name__ == '__main__':
    unittest.main()
