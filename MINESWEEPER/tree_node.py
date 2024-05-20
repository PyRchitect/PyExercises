import collections as cl

rounding = 0

# Tree Class

class TreeNode():
	inorder_split = lambda x: int(x/2) # inorder left-right split
	print_indent = 1

	def __init__(self,data=None,):
		self.data = data
		self.parent = None
		self.children = []

	def isRoot(self):
		return True if self.parent == None else False
	
	def makeRoot(self):
		self.parent = None
	
	def fetchRoot(self):
		fetch_root = self
		while not fetch_root.isRoot(): fetch_root = fetch_root.parent
		return fetch_root
	
	def isLeaf(self):
		return True if self.children == [] else False
	
	def hasParents(self):
		return True if not self.parents() else False

	def parents(self):
		if self.isRoot(): return []

		parents_list = []
		current = self.parent
		while True:
			parents_list.append(current)
			if current.isRoot(): break
			current = current.parent
		
		return parents_list

	def node_level(self):
		return len(self.parents())
	
	def hasChildren(self):
		return True if any(self.children) else False

	def loopChildren(self):
		for child in self.children: yield child
	
	def firstChild(self):
		return None if self.isLeaf() else self.children[0]
	
	def isFirstChild(self):
		return True if (self.isRoot() or self == self.parent.firstChild()) else False

	def lastChild(self):
		return None if self.isLeaf() else self.children[-1]
	
	def isLastChild(self):
		return True if (self.isRoot() or self == self.parent.lastChild()) else False

	def whichChild(self):
		return 0 if self.isRoot() else self.parent.children.index(self)

	def isOnlyChild(self):
		return True if (self.isRoot() or len(self.parent.children) == 1) else False

	def addChild(self,child):
		child.parent = self
		self.children.append(child)
	
	def removeChild(self,child):
		child.parent = None
		self.children.remove(child)
	
	def removeFromParent(self):
		self.parent.removeChild(self.parent,self)
	
	def removeChildren(self):
		self.children = []
	
	# TO DO: loopSiblings

	# TRAVERSALS
	# https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/
	#
	#       1
	#    /     \
	#   2       3
	#  / \     / \
	# 4   5   6   7
	#
	# 1. DFS
	# 1.1. preorder		[1,2,4,5,3,6,7]: used to create a copy of the tree
	# 1.2. inorder		[4,2,5,1,6,3,7]: gives nodes in non-decreasing order
	# 1.3. postorder	[4,5,2,6,7,3,1]: used to delete the tree
	# 2. BFS
	# 2.1. level		[1,2,3,4,5,6,7]
	# 2.2. boundary		[1,2,4,5,6,7,3]
	# 2.3. diagonal		[1,3,7,2,5,6,4]
	
	def preorder(self):
		yield self
		for child in self.children:
			yield from child.preorder()
	
	def inorder(self):
		s = TreeNode.inorder_split(len(self.children))
		for child in self.children[:s]:
			yield from child.inorder()
		yield self
		for child in self.children[s:]:
			yield from child.inorder()
	
	def postorder(self):
		for child in self.children:
			yield from child.postorder()
		yield self
				
	def level(self):
		queue = cl.deque()
		queue.append(self)

		while queue:
			node = queue.popleft()
			yield node
			queue.extend(node.children)

	# TO DO: OPERATIONS
	# move
	# copy
	# find

	def printTree(self,traversal_method):
		for current in traversal_method():
			print(f"{' '*TreeNode.print_indent * current.node_level() } -> {current.data:.{rounding}f}")

def main():
	# driver code:
	root = TreeNode(1)
	root.addChild(TreeNode(2))
	root.children[0].addChild(TreeNode(4))
	root.children[0].addChild(TreeNode(5))
	root.addChild(TreeNode(3))
	root.children[1].addChild(TreeNode(6))
	root.children[1].addChild(TreeNode(7))

	# test code:
	TreeNode.print_indent = 4
	print(f"\nPREORDER: {[x.data for x in root.preorder()]}\n")
	root.printTree(root.preorder)
	print(f"\nINORDER: {[x.data for x in root.inorder()]}\n")
	root.printTree(root.inorder)
	print(f"\nPOSTORDER: {[x.data for x in root.postorder()]}\n")
	root.printTree(root.postorder)
	print(f"\nLEVEL: {[x.data for x in root.level()]}\n")
	root.printTree(root.level)


if __name__ == '__main__':
	main()
