from enum import Enum

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
			ins_param_str = ins_str.split(',')
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

	def apply(self, xml_string: str) -> str:
		pass


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
		self.location = location.split("/")
		self.value = value

	def getLocation(self) -> str:
		return self.location
