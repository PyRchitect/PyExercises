def horner(A,x_0):
	# p(x) = a_0*x^0 + a_1*x^1 + ... + a_n*x^n
	# https://en.wikipedia.org/wiki/Horner%27s_method
	# p(x) = a_0 + x*(a_1 + x*(a_2 + ... + x*(a_n-1 + x*a_n)))
	
	# define b recursively
	# b_n := a_n
	# b_n-1 := a_n-1 + b_n*x_0
	# ...
	# b_1 := a_1 + b_2*x_0
	# b_0 = a_0 + b_1*x_0

	# p(x_0) = a_0 + x_0*(a_1 + x_0*(a_2 + ... + x_0(a_n-1 + b_n*x_0))) = ... = b_0
	# https://en.wikipedia.org/wiki/Polynomial_remainder_theorem
	# p(x) = (b_1*x^0 + b_2*x^1 + b_n-1*x^(n-2) + b_n*x^(n-1))(x-x_0) + b_0
	# p(x)/(x-x_0) = (b_1*x^0 + b_2*x^1 + b_n-1*x^(n-2) + b_n*x^(n-1)) + p(x_0)/(x-x_0)
	
	# https://en.wikipedia.org/wiki/Synthetic_division

	# 		| x^n | x^(n-1) | ...     | x^2     | x^1     | x^0
	#		| a_n | a_(n-1) | ...     | a_2     | a_1     | a_0
	#	x_0	|     | x_0*b_n | ...     | x_0*b_3 | x_0*b_2 | x_0*b_1
	#		+ - - - - - - - - - - - - - - - - - - - - - - - - - - -
	#		| b_n | b_(n-1) | ...     | b_2     | b_1     | b_0

	#		EXAMPLE:
	# 		| x^3 | x^2 | x^1 | x^0
	#		|  2  | -6  |  2  | -1
	#	 3	|     |  6  |  0  |  6
	#		+ - - - - - - - - - - - -
	#		|  2  |  0  |  2  |  5

	#		(2*x^3 -6*x^2 + 2*x^1 -1*x^0)/(x-3) = 2*x^3 + 2*x^1 + 5/(x-3)

	# INPUT:	[a_n, a_(n-1), ..., a_2, a_1, a_0], x_0, ??? rise = -1/1
	# OUTPUT:	[b_n, b_(n-1), ..., b_2, b_1, b_0]
	# q(x) = output[:-1], r(x) = p(x_0) = output[-1]

	# variations using:
	# functools reduce (https://docs.python.org/3/library/functools.html)
	# itertools accumulate (https://docs.python.org/3/library/itertools.html)

	result = [A[0]]
	for i in range(1,len(A)):
		result.append(A[i]+result[i-1]*x_0)
	
	return result

def horner_test(test_list = None, test_value = None):
	test_list = test_list or [2,-6,2,-1]
	test_value = test_value or 3

	def compose_poly_backup(P):
		e = ''
		for i,x in enumerate(P):
			e += f"{'+' if x>=0 else '-'} {abs(x)}*x^{len(P)-1-i} "
		return e

	def compose_poly(P):
		return ''.join([f"{'+' if x>=0 else '-'} {abs(x)}*x^{len(P)-1-i} " for i,x in enumerate(P)])
	
	print("\nHORNER")
	print(f"> POLYNOM: p(x) = {compose_poly(test_list)}")
	divisor = compose_poly([1,-test_value])	# monic poly
	print(f"> DIVISOR: d(x) = {divisor}")
	result = horner(test_list,test_value)
	print(f"> RESULT:  q(x) = {compose_poly(result[:-1])}")
	print(f"> REMAIN:  r(x) = {compose_poly([result[-1]])}/({divisor})")
	print(f"> EVAL@x0: p({test_value}) = {result[-1]}")