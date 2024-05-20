import operator as op

def binary_search(x,A,mode=1,reverse=False):
	# = ascending + descending
	# default mode is 1 because it comforms to how list.insert works
	if mode not in [-1,1]: raise ValueError

	start=0
	end=len(A)-1
	
	if mode == -1:
		# largest smaller (left) if x not in list
		# last index of element if x is in list
		# expects inserting from the right of result
		compare = op.le if reverse else op.lt
	elif mode == 1:
		# smallest larger (right) if x not in list
		# first index of element if x is in list
		# expects inserting from the left of result
		compare = op.lt if reverse else op.le

	def binary_loop(x,start,end):
		if start<end:
			mid=int((start+end)/2)
			if compare(x,A[mid + (1 if mode==-1 else 0)]):
				return binary_loop(x,mid+1,end) if reverse else binary_loop(x,start,mid)
			else:
				return binary_loop(x,start,mid) if reverse else binary_loop(x,mid+1,end)
		else:			
			return start

	return binary_loop(x,start,end)

def binary_search_ascending(x,A,mode=1):

	start=0
	end=len(A)-1
	
	if mode == -1:
		compare = op.lt
	elif mode == 1:
		compare = op.le

	def binary_loop(x,start,end):
		if start<end:
			mid=int((start+end)/2)
			if compare(x,A[mid + (1 if mode==-1 else 0)]):
				return binary_loop(x,start,mid)
			else:
				return binary_loop(x,mid+1,end)
		else:			
			return start

	return binary_loop(x,start,end)

def binary_search_descending(x,A,mode=1):

	start=0
	end=len(A)-1
	
	if mode == -1:
		compare = op.le
	elif mode == 1:
		compare = op.lt

	def binary_loop(x,start,end):
		if start<end:
			mid=int((start+end)/2)
			if compare(x,A[mid + (1 if mode==-1 else 0)]):
				return binary_loop(x,mid+1,end)
			else:
				return binary_loop(x,start,mid)
		else:			
			return start

	return binary_loop(x,start,end)