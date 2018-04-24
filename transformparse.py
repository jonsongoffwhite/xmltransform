from enum import Enum
from xmlparse import XMLParser
import xml.etree.ElementTree as ElementTree
import logging
import sys
import tree_operations as to

class TransformParser:

    def __init__(self, transform_string):
        self.transform_string = transform_string

        # Set up instruction queue

    def _get_instruction_strings(self) -> list:
        stack = []
        elems = []
        start_char = '['
        end_char   = ']'

        curr_str = ""
        for c in self.transform_string:

            if c == start_char:
                stack.append(start_char)

            if c == end_char:
                stack.pop()

            curr_str += c

            # Need to account for other whitespace characters
            if len(stack) == 0 and c != '\n':
                elems.append(curr_str)
                curr_str = ""

        if len(stack) != 0:
            # Return empty list for invalid strings
            # even if some valid
            return []

        return elems

    def _create_instructions(self, instruction_strings) -> list:


        logging.basicConfig( stream=sys.stderr )
        logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
        log= logging.getLogger( "SomeTest.testSomething" )

        ins = []
        for ins_str in instruction_strings:
            # This is all bad because of text
            # Remove square brackets
            ins_str = ins_str.lstrip()[1:-1]
            # Split on first 2 so won't interfere with text
            # Only splits on 1 remove
            ins_param_str = ins_str.split(',', 2)
            # Remove space if at start
            new_param_str = []
            for elem in ins_param_str:
                if len(elem) > 0 and elem[0] == ' ':
                    elem = elem[1:]
                new_param_str.append(elem)
            # Create Instruction
            command = Command.get_command_from_str(new_param_str[0])
            location = new_param_str[1]

            # Check, as remove only has 2 params
            if len(new_param_str) > 2:
                value = new_param_str[2]
            else:
                value = ""
            ins.append(Instruction(command, location, value))

        return ins


    def parse(self) -> list:
        instruction_strings = self._get_instruction_strings()
        instructions = self._create_instructions(instruction_strings)
        return instructions

    def apply(self, instructions: list, xml_string: str) -> str:

        logging.basicConfig( stream=sys.stderr )
        logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
        log= logging.getLogger( "SomeTest.testSomething" )

        xmlparser = XMLParser(xml_string)
        tree = xmlparser.get_tree()
        for ins in instructions:
            root = tree.getroot()

            if ins.command == Command.RENAME:
                if ins.has_attribute_destination():
                    # Don't really want to pass attrib name
                    old_attrib_name = ins.locations[-1][0][1:]
                    log.debug(old_attrib_name)
                    to.get_parent_and_apply(root, ins.locations, to.transform_rename_attrib, new_name=ins.value, attrib=old_attrib_name)
                else:
                    to.get_node_and_apply(root, ins.locations, to.transform_rename_tag, new_name=ins.value)

            elif ins.command == Command.UPDATE:
                # Either starts with @ indicating attribute,
                # or is text() indicating text value
                if ins.has_attribute_destination():
                    attrib_name = ins.locations[-1][0][1:]
                    to.get_parent_and_apply(root, ins.locations, to.transform_update_attrib, attrib=attrib_name, value=ins.value)
                elif ins.has_text_destination():
                    contained_name = ins.locations[-1][0][:-2] 
                    index = ins.locations[-1][1]
                    to.get_parent_and_apply(root, ins.locations, to.transform_update_contained, contained=contained_name, index=index, value=ins.value)  
                    

            elif ins.command == Command.APPEND_FIRST:
                to.get_node_and_apply(root, ins.locations, to.transform_append_first, value=ins.value)

            elif ins.command == Command.APPEND:
                to.get_node_and_apply(root, ins.locations, to.transform_append, value=ins.value)

            elif ins.command == Command.INSERT_AFTER:
                if ins.has_text_destination():
                    # Find index of tag after text()[i]
                    # Insert there
                    contained_name = ins.locations[-1][0][:-2]
                    contained_index = ins.locations[-1][1]
                    value = ins.value
                    to.get_parent_and_apply(root, ins.locations, to.transform_insert_after_contained, contained_name=contained_name, contained_index=contained_index, value=value)

                else:
                    tag_name = ins.locations[-1][0]
                    tag_index = ins.locations[-1][1] 
                    value = ins.value
                    to.get_parent_and_apply(root, ins.locations, to.transform_insert_after_tag, tag_name=tag_name, tag_index=tag_index, value=value)
                    
            elif ins.command == Command.MOVE_FIRST:
                # Pre parsed in Instruction constructor
                new_location = ins.value
                tree_root = root
                src_name = ins.locations[-1][0]
                src_index = ins.locations[-1][1]
                to.get_parent_and_apply(root, ins.locations, to.transform_move_first, new_location=new_location, tree_root=tree_root, src_name=src_name, src_index=src_index)

            elif ins.command == Command.MOVE_AFTER:
                curr = root
                for loc in ins.locations[1:-1]:
                    curr = curr.findall(loc[0])[loc[1]]
                src_parent = curr
                src_loc = ins.locations[-1]
                src = curr.findall(src_loc[0])[src_loc[1]]
                curr = root
                for loc in ins.value[1:-1]:
                    curr = curr.findall(loc[0])[loc[1]]
                dst = curr
                indices = [i for i, x in enumerate(dst) if x.tag == ins.value[-1][0]]
                new_index = indices[ins.value[-1][1]] + 1
                src_parent.remove(src)
                dst.insert(new_index, src)

            elif ins.command == Command.REMOVE:
                curr = root
                for loc in ins.locations[1:-1]:
                    curr = curr.findall(loc[0])[loc[1]]
                # Iterate through to get correct contained index
                if ins.has_text_destination():
                    texts = []
                    # Get texts only at current level inside curr
                    # (node, string, isTail)
                    for node in curr.iter():
                        if node == curr:
                            texts.append((node, node.text, False))
                        else:
                            texts.append((node, node.tail, True))
                    relevant_segment = texts[final_loc[1]]

                    if relevant_segment[2]:
                        relevant_segment[0].tail = None
                    else:
                        relevant_segment[0].text = None
                else:
                    parent = curr
                    loc = ins.locations[-1]
                    rem = curr.findall(loc[0])[loc[1]]
                    parent.remove(rem)

        return tree




class Command(Enum):
    RENAME = 'rename'
    UPDATE = 'update'
    APPEND_FIRST = 'append-first'
    APPEND = 'append'
    INSERT_AFTER = 'insert-after'
    MOVE_FIRST = 'move-first'
    MOVE_AFTER = 'move-after'
    REMOVE = 'remove'

    @staticmethod
    def get_command_from_str(str):
        for c in list(Command):
            if c.value == str:
                return c
        return None

class Instruction:

    def __init__(self, command: Command, location: str, value: str):
        self.command = command

        # Remove first empty string
        self.locations = self._split_location(location)

        # Value is also a location in these cases
        if command == Command.MOVE_FIRST or command == Command.MOVE_AFTER:
            self.value = self._split_location(value)
        else:
            self.value = value.lstrip()


    def _split_location(self, location_str) -> list:
        location_strs = location_str.split("/")[1:] 
        locations = []

        for location in location_strs:
            # Root case
            if len(location) == 0:
                dir_ = ""
                index_int = -1
            # Final location might be special
            elif location[0] == '@':# or location[-2:] == '()':
                dir_ = location
                index_int = -1
            else:
                # Separate index and dir
                dir_  = location.split('[')[0]
                # If there is an index, parse it, otherwise -1
                if len(location.split('[')) == 1:
                    index_int = -1
                else:
                    index_str = location.split('[')[1].split(']')[0]
                    index_int = int(index_str)-1
            locations.append((dir_, index_int))

        return locations

    def has_attribute_destination(self):
        return self.locations[-1][0][0] == '@'

    def has_contained_destination(self):
        return self.locations[-1][-2:][0] == '()'

    def has_text_destination(self):
        return self.locations[-1][-2:][0] == 'text()'


    def getLocation(self) -> str:
        return self.location

    def __str__(self) -> str:
        return str(self.__dict__)
