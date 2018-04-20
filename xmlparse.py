import xml.etree.ElementTree as ElementTree

class XMLParser:

	def __init__(self, xml, from_file=False):
		if from_file:
			self.filename = xml
			try:
				self.etree = ElementTree.parse(xml)
				self.root = self.etree.getroot()
			except FileNotFoundError:
				print("file not found:")
				print(error)
				return
		else:
			self.root = ElementTree.fromstring(xml)
			self.etree = ElementTree.ElementTree(self.root)

	def get_tree(self):
		return self.etree

	def get_string(self):
		return ElementTree.tostring(self.root, encoding="unicode")

	def writeTreeToFile(self, dst):
		self.etree.write(dst)

