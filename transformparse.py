from enum import Enum
from xmlparse import XMLParser
import logging
import sys

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

			if len(stack) == 0:
				elems.append(curr_str)
				curr_str = ""

		if len(stack) != 0:
			# Return empty list for invalid strings
			# even if some valid
			return []

		return elems

	def _create_instructions(self, instruction_strings) -> list:
		ins = []
		for ins_str in instruction_strings:
			# Remove square brackets
			ins_str = ins_str[1:-1]
			# Split by comma
			ins_param_str = ins_str.replace(" ", "").split(',')
			# Create Instruction
			command = Command.get_command_from_str(ins_param_str[0])
			location = ins_param_str[1]
			value = ins_param_str[2]
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
				curr = root
				# Skip root
				for loc in ins.locations[1:]:
					curr = curr.findall(loc[0])[loc[1]]
				curr.tag = ins.value

			elif ins.command == Command.UPDATE:
				# Either starts with @ indicating attribute,
				# or is text() indicating text value
				curr = root
				final_loc = ins.locations[-1]
				# Skip root
				for loc in ins.locations[1:-1]:
					curr = curr.findall(loc[0])[loc[1]]
				if final_loc[0][0] == '@':
					curr.attrib[final_loc[0][1:]] = ins.value
				elif final_loc[0][-2:] == '()' and final_loc[0][:-2] == 'text':
					curr.text = ins.value


		return xmlparser.get_string()




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

		locations = location.split("/")[1:] # Remove first empty string
		self.locations = []
		for location in locations:

			# Final location might be special
			if location[0] == '@' or location[-2:] == '()':
				dir_ = location
				index_int = -1
			else:
			# Separate index and dir
				dir_  = location.split('[')[0]
				index_str = location.split('[')[1].split(']')[0]
				index_int = int(index_str)-1
			self.locations.append((dir_, index_int))

		self.value = value

	def getLocation(self) -> str:
		return self.location
