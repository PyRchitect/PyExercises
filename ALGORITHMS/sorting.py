import random as rn
import operator as op
import collections as cl

import binary_search

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <LIB>

def get_list(test_list=None):
	if not test_list:
		list_length = 10	# list_length = input("List length: ")
		lower_bound = 0		# lower_bound = input("Lower bound: ")
		upper_bound = 100	# upper_bound = input("Upper bound: ")

		return rn.choices(range(lower_bound,upper_bound),k=list_length)
	return test_list

def swap_by_index(A,x,y):
	t = A[x]
	A[x] = A[y]
	A[y] = t

# </LIB>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# <SORTING ALGORITHMS COMPARISON>

def insertion_sort_while_loop(L,reverse=False):
	# while loop insertion sort
	compare = op.lt if reverse else op.gt

	for i in range(1,len(L)):
		key = L[i]
		j = i-1
		while j>=0 and compare(L[j],key):
			L[j+1]=L[j]
			j=j-1
		L[j+1]=key

def insertion_sort_recursive(A,reverse=False):
	# recursive insertion sort
	compare = op.lt if reverse else op.gt

	if len(A)>=1:
		key = [A[-1]]					# convert to list for convenience
		T = cl.deque(list(A)[:-1])		# faster than list object
		insertion_sort_recursive(T,reverse)	# sort list [0,n-1]

		for k in range(len(T)+1):
			if T and key:
				A[k]=T.popleft() if compare(key[0],T[0]) else key.pop()
			elif T:
				while T:
					A[k]=T.popleft()	# empty the queue from left
					k+=1				# while advancing the index
				break
			else:
				A[k]=key.pop()

def insertion_sort_binary(L,reverse=False):
	# iterative insertion sort with binary search	
	compare = op.lt if reverse else op.gt	
	
	for i in range(1,len(L)):
		if compare(L[i-1],L[i]):
			key = L.pop(i)
			j = binary_search(key,L[:i],reverse=reverse)
			L.insert(j,key)

def selection_sort(A,reverse=False):
	# in-place selection sort
	compare = op.lt if reverse else op.gt

	for x in range(len(A)-1):
		min = x
		for y in range(x,len(A)):			
			if compare(A[min],A[y]):
				min = y
		if min != x: swap_by_index(A,x,min)

def bubble_sort(A,reverse=False):
	# in-place bubble sort
	compare = op.lt if reverse else op.gt
	
	for x in range(len(A)-1):
		for y in range(len(A)-1,x,-1):
			if compare(A[y-1],A[y]):
				swap_by_index(A,y,y-1)

def merge_sort_while_loop(A,reverse=False):

	compare = op.ge if reverse else op.le

	if len(A)>1:
		mid=len(A)//2
		L=A[:mid]
		R=A[mid:]
		merge_sort(L,reverse)
		merge_sort(R,reverse)

		i=j=k=0
		while i<len(L) and j<len(R):
			if compare(L[i],R[j]):
				A[k]=L[i]
				i+=1
			else:
				A[k]=R[j]
				j+=1
			k+=1
		while i<len(L):
			A[k]=L[i]
			i+=1
			k+=1
		while j<len(R):
			A[k]=R[j]
			j+=1
			k+=1

def merge_sort(A,reverse=False):

	compare = op.ge if reverse else op.le

	if len(A)>1:
		mid=len(A)//2
		
		# L=cl.deque(it.islice(A,0,mid))
		L=cl.deque(list(A)[:mid])
		# R=cl.deque(it.islice(A,mid,len(A)))
		R=cl.deque(list(A)[mid:])
		merge_sort(L,reverse)
		merge_sort(R,reverse)

		for k in range(len(L)+len(R)):
			if L and R:
				A[k]=L.popleft() if compare(L[0],R[0]) else R.popleft()
			elif L:
				# A[k]=L.popleft()
				while L:
					A[k]=L.popleft()	# empty the queue from left
					k+=1				# while advancing the index
				break
			elif R:
				# A[k]=R.popleft()
				while R:
					A[k]=R.popleft()	# empty the queue from left
					k+=1				# while advancing the index
				break

def sort_test(sort_type,test_list=None,reverse=False):
	test_list = get_list(test_list)

	print(f"\n> {sort_type.__name__} test: {'decreasing' if reverse else 'increasing'}")
	print(f"Test: {test_list}")
	sort_type(test_list,reverse)
	print(f"Sort: {test_list}")

# </SORTING ALGORITHMS COMPARISON>