import random as rn
import collections as cl

def get_list(test_list=None):
	if not test_list:
		list_length = 10	# list_length = input("List length: ")
		lower_bound = 0		# lower_bound = input("Lower bound: ")
		upper_bound = 100	# upper_bound = input("Upper bound: ")

		return rn.choices(range(lower_bound,upper_bound),k=list_length)
	return test_list

def inversions(A):
	# Let A[1:n] be an array of n distinct numbers.
	# If i < j and A[i] > A[j], then the pair
	# (i,j) is called an inversion of A.

	# Give an algorithm that determines the number of inversions
	# in any permutation on n elements in O(n*lgn) worst-case time.
	# (Hint: Modify merge sort.)

	inversions_counter = 0

	def calculate_inversions(A):
		nonlocal inversions_counter

		if len(A)>1:
			mid=len(A)//2
			
			# L=cl.deque(it.islice(A,0,mid))
			L=cl.deque(list(A)[:mid])
			# R=cl.deque(it.islice(A,mid,len(A)))
			R=cl.deque(list(A)[mid:])
			calculate_inversions(L)
			calculate_inversions(R)

			for k in range(len(L)+len(R)):
				if L and R:
					if L[0]>R[0]:
						A[k]=R.popleft()
						inversions_counter += len(L)
					else:
						A[k]=L.popleft()
				elif L:
					while L:
						A[k]=L.popleft()	# empty the queue from left
						k+=1				# while advancing the index
					break
				elif R:
					while R:
						A[k]=R.popleft()	# empty the queue from left
						k+=1				# while advancing the index
					break
	
	calculate_inversions(A)
	return inversions_counter

def inversions_test(n):
	test_group = [get_list() for x in range(n)]
	# test_group = [[1,2,3,4,5,6],[1,3,2,4,6,5],[6,5,4,3,2,1]]	

	for l in test_group:
		print(f"\nTEST LIST:  {l}")
		print(f"INVERSIONS: {inversions(l)}")