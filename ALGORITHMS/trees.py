import random as rn
import sys

rounding = 0
test_trial_probability = 0.4

# Tree Class

class TreeNode():
	max_children = 0

	def __init__(self,data=None,inorder_split=lambda x: int(x/2)):
		self.data = data
		self.parent = None
		self.children = []
		self.inorder_split = inorder_split # inorder left-right split

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

	# TO DO: loopSiblings > nakon iter

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
		s = self.inorder_split(len(self.children))
		for child in self.children[:s]:
			yield from child.inorder()
		yield self
		for child in self.children[s:]:
			yield from child.inorder()
	
	def postorder(self):
		for child in self.children:
			yield from child.postorder()
		yield self

	# TO DO: OPERATIONS
	# move
	# copy
	# find

	def printTree(self,traversal_method):
		for current in traversal_method():
			print(f"{' '*8 * current.node_level() } -> {current.data:.{rounding}f}")

# Binary Tree Class
class BinaryTreeNode(TreeNode):
	max_children = 2

	def __init__(self,data=None):
		self.trajectory = []
		TreeNode.__init__(self,data)

	def left(self): return self.firstChild()

	def right(self): return self.lastChild()

	def addChild(self,child):
		if len(self.children) == self.max_children:
			raise IndexError(f"greska: broj djece je vec maksimalan ({self.max_children})")
		else:
			child.parent = self
			self.children.append(child)

	@staticmethod
	def sequential_search(node,guide,start,end,step=1):

		if start==end: return StopIteration # test - zadnji krug?
		#if start==end: return 0

		mid = int((start+end)/2)

		if guide>=start and guide<=mid:
			yield (node,0)
			yield from BinaryTreeNode.sequential_search(node.left(),guide,start,mid,step+1)
		else:
			yield (node,1)
			yield from BinaryTreeNode.sequential_search(node.right(),guide,mid+1,end,step+1)

	def populate_tree(self):
		raise NotImplementedError('svaka podklasa mora definirati vlastiti način')

	@staticmethod
	def printBinaryTree(node,level=0):
		if node != None:
			BinaryTreeNode.printBinaryTree(node.left(),level+1)
			print(f"{' '*8 * level} -> {node.data:.{rounding}f}, {node.trajectory}")
			BinaryTreeNode.printBinaryTree(node.right(),level+1)

# Probability Binary Tree Class        
class PBinaryTreeNode(BinaryTreeNode):

	def populate_tree(self,input_method,probability_assignment,tree_depth,search_method):

		# INPUT METHODS (random, input, file):

		# 0. simple random assignment, float with 2 decimal places
		input_random = lambda : round(rn.random(),rounding)

		# 1. expects user input
		input_user = lambda : float(input(f" unesi vrijednost: "))

		# 2. expects input from file
		def input_file():           
			with open(sys.path[0]+'\\'+'data.txt') as f: # TEMP, nebitno
				for l in f: yield float(l)

		input_method_options = {0:input_random,1:input_user,2:input_file}
		# FROM HERE: expand to download from service, from SQL DB, from XL, ...

		# PROBABILITY ASSIGNMENT (fixed, dynamic):

		# 0. fixed - i.e. binomial distribution
		if probability_assignment == 0:
			# set probability beforehand
			fixed_probability = input_method_options[input_method]()

			# TEST
			# fixed_probability = test_trial_probability
			# TEST
		
		# 1. dynamic - custom distribution
		# require input for each node       

		# SEARCH METHODS (sequential, ... DFS, BFS, LS)
		if search_method == 0:
			search_args = (1,pow(2,tree_depth))     # true range for guide
			range_args = (1,pow(2,tree_depth)+1)    # ! range needs +1 (last)

		search_method_options = {0:BinaryTreeNode.sequential_search}
		# FROM HERE: expand to DFS, BFS, LS, ...

		start_node = self
		# just in case:
		start_node.makeRoot()
		start_node.children = []

		for x in list(range(*range_args)):
			for (current,next_move) in search_method_options[search_method](start_node,x,*search_args):
				if len(current.children) <= (next_move):
					# check next move (0 = left, 1 = right):
					# if no children:
					# # if next move 0 > add child
					# # if next move 1 > add child
					# if one child:
					# # if next move 0 > move on
					# # if next move 1 > add child
					# if two children:
					# # if next move 0 > move on
					# # if next move 1 > move on
					current.addChild(PBinaryTreeNode())
					# add child with empty data

					# if len(current.children)==1:
					if current.children[0].isOnlyChild():
						# if first child added, populate with chosen method
						if probability_assignment == 0:
							# if fixed, assign it to node
							node_data = fixed_probability
						else:
							# if dynamic, set for this node
							node_data = input_method_options[input_method]()
					else:
						node_data = 1 - current.firstChild().data
						# if second child added, take 1 minus first child
					current.lastChild().data = node_data
					current.lastChild().trajectory = current.trajectory+[next_move]

	def calculate_trajectories(root_node,tree_depth,chosen_trajectories=None):

		search_args = (1,pow(2,tree_depth))     # true range for guide
		range_args = (1,pow(2,tree_depth)+1)    # ! range needs +1 (last)

		checklist = chosen_trajectories or list(range(*range_args))

		calculated_trajectories=[[],[]]

		for x in checklist:
			product = 1
			sum = 0

			for (current,next_move) in BinaryTreeNode.sequential_search(root_node,x,*search_args):
				if next_move == 0:
					product *= current.left().data
				else:
					product *= current.right().data
				sum+=next_move

			calculated_trajectories[0].append(product)
			calculated_trajectories[1].append(sum)
		
		return calculated_trajectories

# MAIN

def print_trajectories(chosen,calculated):    
			
	for t in zip(chosen,*calculated):    
		print(f"Trajectory {t[0]}: P = {t[1]:.{rounding}f}, sum = {t[2]}")    

def PBT_test():

	def test_random():

		print("\n TEST: RANDOM")

		pbt = PBinaryTreeNode(1)
		depth = 3

		pbt.populate_tree(0,1,depth,0)

		print("\n> tree:")
		PBinaryTreeNode.printBinaryTree(pbt.fetchRoot())

		# CALCULATE TRAJECTORIES

		print("\n> example: all")
		custom_trajectories = list(range(1,pow(2,depth)+1))
		result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth)
		print_trajectories(custom_trajectories,result)

		print("\n> example: hardcode 1,4")
		custom_trajectories = [1,4]
		result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth,custom_trajectories)
		print_trajectories(custom_trajectories,result)

		print("\n> example: comprehension - evens")
		custom_trajectories = [x for x in range(1,pow(2,depth)+1) if x%2==0]
		result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth,custom_trajectories)
		print_trajectories(custom_trajectories,result)
	
	def test_binomial():        

		print("\n TEST: BINOMIAL")

		pbt = PBinaryTreeNode(1)
		depth = 5

		pbt.populate_tree(0,0,depth,0)

		print("\n> STABLO (VJEROJATNOSTI):")
		PBinaryTreeNode.printBinaryTree(pbt.fetchRoot())

		# CALCULATE TRAJECTORIES

		print("\n> REZULTAT (TRAJEKTORIJE):")
		custom_trajectories = list(range(1,pow(2,depth)+1))
		result = PBinaryTreeNode.calculate_trajectories(pbt.fetchRoot(),depth)
		print_trajectories(custom_trajectories,result)

		# SUM OVER TRAJECTORIES WITH SAME SUM (same number of L and D)

		print("\n> REZULTAT (KUMULATIV):")
		cumulative = [0]*(depth+1)

		for x in zip(result[0],result[1]): cumulative[x[1]]+=x[0]
		for i,c in enumerate(cumulative): print(f"[{depth-i}xL,{i}xD] P = {c:.{rounding}f}")

		# from numpy import random as np_rd
		# x = np_rd.binomial(n=depth,p=0.5,size=depth)
		# print(x)

		print("\n> TEST (BINOMIAL):")
		from scipy.stats import binom
		for i,x in enumerate(range(depth+1)): 
			p = binom.pmf(k=x,n=depth,p=test_trial_probability)
			print(f"[{i}xL,{depth-i}xD] P = {p:.{rounding}f}")

	test_random()

	test_binomial()

def T_test():
	# driver code:
	root = TreeNode(1)
	root.addChild(TreeNode(2))
	root.children[0].addChild(TreeNode(4))
	root.children[0].addChild(TreeNode(5))
	root.addChild(TreeNode(3))
	root.children[1].addChild(TreeNode(6))
	root.children[1].addChild(TreeNode(7))

	print("\n\nPREORDER")
	root.printTree(root.preorder)
	print([x.data for x in root.preorder()])
	print("\n\nINORDER")
	root.printTree(root.inorder)
	print([x.data for x in root.inorder()])
	print("\n\nPOSTORDER")
	root.printTree(root.postorder)
	print([x.data for x in root.postorder()])

T_test()
PBT_test()