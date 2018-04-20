import xml.etree.ElementTree as ElementTree

class XMLParser:

	def __init__(self, filename):
		try:
			self.etree = ElementTree.parse(filename)
			self.root = self.etree.getroot()
		except FileNotFoundError:
			print("file not found:")
			print(error)
			return

	def writeTreeToFile(self, dst):
		self.etree.write(dst)

