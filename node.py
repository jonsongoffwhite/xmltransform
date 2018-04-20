

class Node:

	def __init__(self, parent, children, tag, attributes):
		self.parent = parent
		self.children = children
		self.tag = tag
		self.attributes = attributes

	def addChild(self, child):
		self.children.append(child)

	def getDepth(self) -> int:
		if len(children) == 0:
			return 1

		depths = []
		for child in children:
			depths.append(child.getDepth())

		return max(depths) + 1