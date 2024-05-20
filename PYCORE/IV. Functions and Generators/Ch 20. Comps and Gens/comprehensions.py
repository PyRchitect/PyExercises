import sys

# LIST COMPREHENSIONS

def list_comps_vs_map():
    print("\nLIST COMPREHENSIONS VS MAP")

    # ord - returns int code point of a char
    # chr - returns char for an int code point

    print("> collect ASCII codes of all chares in string")

    S = 'spam'
    print(f"> > test string: {S}")

    print("> > with for loop:",end=' ')
    res = []
    for s in S: res.append(ord(s))
    print(res)

    print("> > with map:",end=' ')
    print(list(map(ord,S)))

    print("> > with comp:",end=' ')
    print([ord(s) for s in S])

    print("> applying arbitrary expression to sequence")

    L = range(10)
    print(f"> > test list (range): {list(L)}")

    print("> > square each element:")

    print("> > > with map and lambda",end=' ')
    print(list(map((lambda x : x**2),L)))

    print("> > > with comp",end=' ')
    print([x**2 for x in L])

def list_comps_vs_filter():
    print("\nADDING TESTS AND NESTED LOOPS: FILTER")

    print("> pick up even numbers in range:")

    L = range(10)
    print(f"> > test list (range): {list(L)}")

    print("> > > with for loop:",end=' ')
    res = []
    for l in L:
        if l%2==0:
            res.append(l)
    print(res)

    print("> > > with filter:",end=' ')
    print(list(filter((lambda x : x%2==0),L)))

    print("> > > with comp:",end=' ')
    print([x for x in L if x%2==0])

    print("> square each even, dispose odd:")

    print("> > using filter and map:",end=' ')
    print(list(map((lambda x : x**2),filter((lambda x : x%2==0),L))))

    print("> > with comp:",end=' ')
    print([x**2 for x in L if x%2==0])

def formal_comprehension_syntax():

    # [ expression  for target1 in iterable1 if condition1 ...
    #               for targetK in iterableK if conditionK ...
    #               for targetN in iterableN if conditionN]

    print("> add numbers in multiple lists:")

    L1 = [1,2]; n = 3; L=[]
    for n in range(n):
        L.append([x*(10**n) for x in L1])

    print(f"> > test lists: {L}")

    print("> > with for loop:",end=' ')
    res = []
    for x in L[0]:
        for y in L[1]:
            for z in L[2]:
                res.append(x+y+z)
    print(res)

    print("> > with comp:",end=' ')
    print([x+y+z for x in L[0] for y in L[1] for z in L[2]])

    print("> filter combinations in multiple strings:")

    S1 = 'spam'; S2 = 'SPAM'; S3 = '123'

    print(f"> > test strings: {S1,S2}, filter 'sm','PA'")
    print([x+y  for x in S1 if x in ('sm') 
                for y in S2 if y in ('P','A')])

    print(f"> > test strings: {S1,S2,S3}, filter 'sm','PA',>'1'")
    print([x+y+z    for x in S1 if x in ('s','m')
                    for y in S2 if y in 'PA'
                    for z in S3 if z > '1'])

    print("> create (even,odd) 2-tuples:")
    
    L=range(5)
    print([(x,y)    for x in L if x%2==0
                    for y in L if y%2!=0])

def print_matrix(M):
    max_num_digits = len(str(max([max(x) for x in M])))

    for row in M:
        print("[",end=' ')
        for col in row:            
            pad = ' '*(max_num_digits - len(str(col)))
            print(pad,col,sep='',end=' ')
        print("]")

def list_comps_and_matrices():
    print("\nLIST COMPREHENSIONS AND MATRICES")

    M= [[1,2,3],
        [4,5,6],
        [7,8,9]]

    N= [[2,2,2],
        [3,3,3],
        [4,4,4]]

    print("> test matrices:")
    print("\n> > M"); print_matrix(M)
    print("\n> > N"); print_matrix(N)
    print()

    print("> accessing elements:")
    print(f"> > M, row 2: {M[1]}")
    print(f"> > N, row 1, col 2: {N[0][1]}")

    print("> extracting cols using comps:")
    print(f"> > M, col 2: {[row[1] for row in M]}")
    print(f"> > using offsets: {[M[row][1] for row in (0,1,2)]}")

    print("> pulling diagonals:")
    print(f"> > M, main: {[M[i][i] for i in range(len(M))]}")
    print(f"> > M, other: {[M[len(M)-1-i][i] for i in range(len(M))]}")

    print("> changing in place:")
    update = lambda x : x+10

    print("> > using for loop:")    

    for i in range(len(M)):
        for j in range(len(M[0])):
            M[i][j]=update(M[i][j])
    
    print("\n> > M"); print_matrix(M); print()

    print("> > using inner and outer loop")

    res = []
    for row in M:
        tmp = []
        for col in row:
            tmp.append(update(col))
        res.append(tmp)
    M = res

    print("\n> > M"); print_matrix(M); print()

    print("> > using comp:")

    M = [[update(col) for col in row] for row in M]

    print("\n> > M"); print_matrix(M); print()

    print("> multiply matrix by coefficients:")
    print("\n> > M"); print_matrix(M); print()
    print("\n> > N"); print_matrix(N); print()
    # say you keep main results and some coefs separately
    # you may need to multiply each result with its coef.
    # R[i][j] = M[i][j] * C[i][j] ; aX = a * X for each
    # THIS IS NOT REAL MATRIX MULTIPLICATION ! (see below)

    print("> > using comp:")

    R = [[M[row][col]*N[row][col] for col in range(len(M))] for row in range(len(N))]

    print("\n> > R"); print_matrix(R); print()

    print("> > using for loop:")

    R = []
    for row in range(len(M)):
        tmp = []
        for col in range(len(N)):
            tmp.append(M[row][col]*N[row][col])
        R.append(tmp)

    print("\n> > R"); print_matrix(R); print()

    print("> > using comp with zip:")

    R = [[col1*col2 for (col1,col2) in zip(row1,row2)] for (row1,row2) in zip(M,N)]

    print("\n> > R"); print_matrix(R); print()

    print("> > using for loop with zip:")

    R = []
    for (row1,row2) in zip(M,N):
        tmp = []
        for (col1,col2) in zip(row1,row2):
            tmp.append(col1*col2)
        R.append(tmp)

    print("\n> > R"); print_matrix(R); print()

def matrix_multiplication():
        
    def MM(M,N):
        res=[]
        for i in range(len(M)):
            tmp=[]
            for j in range(len(N[i])):
                S=0
                for k in range(len(M[i])):
                    S+=M[i][k]*N[k][j]
                tmp.append(S)
            res.append(tmp)
        return res
    
    I=[[1,0,0],[0,1,0],[0,0,1]]    

    M= [[1,2,3],
        [4,5,6],
        [7,8,9]]
    
    print(f"\n> > I"); print_matrix(I); print()
    print(f"\n> > M"); print_matrix(M); print()

    print(f"\n> > I*I"); print_matrix(MM(I,I)); print()
    print(f"\n> > I*M"); print_matrix(MM(I,M)); print()
    print(f"\n> > M*I"); print_matrix(MM(M,I)); print()
    print(f"\n> > M*M"); print_matrix(MM(M,M)); print()    

def numpy_multiplication():
    
    import numpy as np

    I = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # M = np.array([[1,2,3],[4,5,6],[7,8,9]])
    M = np.arange(1,10).reshape(3,3)

    print(f"\n> > I*I:"); print(np.matmul(I,I)); print()
    print(f"\n> > I*M:"); print(np.matmul(I,M)); print()
    print(f"\n> > M*I:"); print(np.matmul(M,I)); print()
    print(f"\n> > M*M:"); print(np.matmul(M,M)); print()    

def list_comps_and_map():
    print("\nLIST COMPREHENSIONS AND MAP")

    print("> line stripping for file iterators")

    path = sys.path[0]
    filename = 'data.txt'
    filepath = path + "\\" + filename

    S = open(filepath).readlines()
    print(f"> > readlines data from file: {S}")

    S = [line.rstrip() for line in open(filepath).readlines()]
    print(f"> > use comp to strip newlines: {S}")

    S = [line.rstrip() for line in open(filepath)]
    print(f"> > lines are iterables, read 1 by 1: {S}")

    S = list(map(lambda line : line.rstrip(), open(filepath)))
    print(f"> > same function, with map: {S}")

    print("> column projection operations")

    # standard SQL database API query result returns:
    listoftuple = [('bob',35,'mgr'),('sue',40,'dev')]

    print("> get age, collect in list:")

    print("> > with for loop:",end=' ')
    L = []
    for name,age,pos in listoftuple: L.append(age)
    print(L)

    print("> > with comp:",end=' ')
    print([age for (name,age,pos) in listoftuple])

    print("> > with map:",end=' ')
    print(list(map((lambda x : x[1]),listoftuple)))

# COMPREHENSION SYNTAX SUMMARY

def set_comps():
    print("\nSET COMPREHENSIONS")

    L = [1,2,1,3,1,4]
    S = 'SPAM'

    print("> set syntax:")
    set_l = {1,2,3,4}
    print(f"> literal set syntax: {set_l}")
    set_f = set([1,2,3,4])
    print(f"> function set syntax: {set_f}")

    print("> set comp:")
    set_lc = {x for x in set_l if x>0}
    print(f"> literal set comp: {set_lc}")
    set_fc = set(x for x in set_f if x>0)
    print(f"> function set comp: {set_fc}")

    print("> just syntax for passing gen. exp. to type names")
    set_gc = {*list(x for x in set_l if x>0)}
    print(f"> > gen inside set type: {set_gc}")

    print("> extended comp syntax:")
    set_ec = {x*x for x in range(5) if x%2 == 0}
    print(f"> > collect squares of even numbers: {set_ec}")
    set_oc = {x+y for x in [1,2,3] for y in [4,5,6]}
    print(f"> > filter dups in op on two lists: {set_oc}")

    print("> set comps iterate over any type of iterable:")
    set_sc = {x+y for x in 'ab' for y in 'cd'}
    print(f"> > strings: {set_sc}")
    set_lsc = {k*2 for k in ['spam','ham','sauce'] if k[0]=='s'}
    print(f"> > collect doubles if startswith 's': {set_lsc}")


def dict_comps():
    print("\nDICT COMPREHENSIONS")

    keys = ['k1','k2','k3','k4']
    vals = ['v1','v2','v3','v4']

    print("> dict syntax:")
    dict_l = {'k1':'v1','k2':'v2','k3':'v3','k4':'v4'}
    print(f"> > literal dict syntax:\n{dict_l}")
    dict_f = dict(zip(keys,vals))
    print(f"> > function dict syntax:\n{dict_f}")

    print("> dict comp:")
    dict_lc = {k:v for (k,v) in zip(keys,vals)}
    print(f"> > literal dict comp:\n{dict_lc}")
    dict_fc = dict((k,v) for (k,v) in zip(keys,vals))
    print(f"> > function dict comp:\n{dict_fc}")

    print("> just syntax for passing gen. exp. to type names")
    dict_gc = dict((x,x*x) for x in range(5))
    print(f"> > gen inside dict type: {dict_gc}")

    print("> extended comp syntax:")
    dict_ec = {(x,x*x) for x in range(5) if x%2 == 0}
    print(f"> > collect squares of even numbers: {dict_ec}")
    dict_oc = {x:y for x in [1,2,1,3] for y in [4,5,4,6]}
    print(f"> > filter dups in op on two lists: {dict_oc}")

    print("> dict comps iterate over any type of iterable:")
    dict_sc = {x+y:(ord(x),ord(y)) for x in 'ab' for y in 'cd'}
    print(f"> > strings: {dict_sc}")
    set_lsc = {k.upper():k*2 for k in ['spam','ham','sauce'] if k[0]=='s'}
    print(f"> > collect upper:doubles if startswith 's': {set_lsc}")

def scopes_and_comp_vars():
    print("\nSCOPES AND COMPREHENSION VARIABLES")    

    x = 1
    print(f"> test variable: {x}")

    G = (x for x in range(5))
    L = [x for x in range(5)]
    S = {x for x in range(5)}
    D = {x:x**2 for x in range(5)}
    print(f"> comps localize (after G,L,S,D): {x}")

    for x in range(5): pass
    print(f"> loops don't localize (after for): {x}")

set_comps()
dict_comps()
scopes_and_comp_vars()