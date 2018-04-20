from enum import Enum

class TransformParser:

	def __init__(self, filename):
		self.filename = filename

		# Set up instruction queue

	def parse(self):
		pass


class Command(Enum):
	RENAME = 1
	UPDATE = 2 
	APPEND_FIRST = 3
	APPEND = 4
	INSERT_AFTER = 5
	MOVE_FIRST = 6
	MOVE_AFTER = 7
	REMOVE = 8

class Instruction:

	def __init__(self, command: Command, location: str, value: str):
		self.command = command
		self.location = location.split("/")
		self.value = value

	def getLocation(self) -> str:
		return self.location
