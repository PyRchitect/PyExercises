def get_last_index(x,L):
	#
	# find last occurence of element in list:
	# next((i for i in reversed(range(len(L))) if L[i] == x),None)
	#
	# creates a generator over 0-to-list len, going backwards (reversed)
	# finds first occurrence where element value equals searched item, exits
	# returns the index if search succeeds or returns None if x not in list
	# the condition to yield new element is it being equal to searched item!
	#
	return next((i for i in reversed(range(len(L))) if L[i] == x),None)