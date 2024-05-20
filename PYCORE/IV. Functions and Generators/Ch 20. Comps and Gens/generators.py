import os
import sys

def gen_func():
    print("\nGENERATOR FUNCTIONS")

    def gen_squares(N):
        for i in range(N):
            yield i**2

    n = 5
    print(f"> generate squares of values up to {n}:",end=' ')
    for i in gen_squares(n):
        print(i,end=' : ')
    print()

    print("> initialize the generator")
    x = gen_squares(5)
    print("> advance the generator:")
    print(f"> > {x.__next__()}")
    print(f"> > {x.__next__()}")
    print(f"> > {x.__next__()}")
    print(f"> > {x.__next__()}")
    print(f"> > {x.__next__()}")
    # print(f"> > {x.__next__()}")
    # raises StopIteration

    print("> generator is its own iterator")
    print(f"> > iter(x) = x ? {iter(x) is x}")
    
    print("> build squares of values (all at once!):")
    print("> > with separate def:",end=' ')

    def build_squares(N):
        res = []
        for i in range(N):
            res.append(i**2)
        return res
    
    for i in build_squares(n):
        print(i,end=' : ')
    print()

    print("> > with map and lambda:",end=' ')
    for i in map((lambda x : x**2),range(n)):
        print(i,end=' : ')
    print()

    print("> > with comp:",end=' ')
    for i in [x**2 for x in range(n)]:
        print(i,end=' : ')
    print()

    print("> > directly:",end=' ')
    for i in range(n):
        print(i**2,":",end=' ')
    print()

    print("> substring generator:")

    def ups(L):
        for line in L.split(','):
            yield line.upper()

    S = "aaa,bbb,ccc"
    print(f"> > test string: {S}, split (','), upper:")    

    print("> > > with for loop:",end=' ')
    for sub in ups(S):
        print(sub,end=' ')
    print()
    
    print(f"> > > convert to tuple:",end=' ')
    print(tuple(ups(S)))

    print(f"> > > generate dict:",end=' ')
    print({i:s for (i,s) in enumerate(ups(S))})

    print("> send vs next")
    # send advances to the next item, also sends data to generator
    # > yield exp. in the gen. returns the value passed to send
    # > if the regular next is called, the yield simply returns None

    def gen_test():
        for i in range(10):
            x = yield i
            print(x)
    
    G = gen_test()
    print("> > initialize the generator")
    # must call next first to start the gen
    print(f"> > > {G.__next__()}")
    print(f"> > >",end=' '); G.send(77)
    print(f"> > >",end=' '); G.send(88)
    print(f"> > > {G.__next__()}")

def gen_exp():
    print("\nGENERATOR EXPRESSIONS")

    print("> building a list of squares up to n:")
    n = 5

    print("> > with comp (all at once!):",end=' ')
    print([x**2 for x in range(n)])

    print("> > with generator (force list):",end=' ')
    G = (x**2 for x in range(n))
    print(list(G))
    print(G)

    print("> > with generator (1 by 1):")
    G = (x**2 for x in range(n))
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    # print(f"> > > {G.__next__()}")
    # raises StopIteration

    print("> > with generator (for loop):")
    G = (x**2 for x in range(n))
    for g in G: print(f"> > > {g}")

    print("> > sum iteraton context: sum =",end=' ')
    G = (x**2 for x in range(n))
    print(sum(G))

    print("> > sorted iteration context (reverse):",end=' ')
    G = (x**2 for x in range(n))
    print(sorted(G,reverse=True))

    print(f"> > iter(G) is G ? {iter(G) is G}")

    print("\n> string iteration with generators")

    S = "aaa,bbb,ccc"
    print(f"> > test string: {S}")

    print("> string join iteration context")

    print(f"> > joined string (split ','):",end=' ')
    print(''.join(x.upper() for x in S.split(',')))

    print("> tuple assignment iteration context")

    a,b,c = (x for x in S.split(','))
    print("> > assigned values (split ','):")
    print(f"> > > {a}")
    print(f"> > > {b}")
    print(f"> > > {c}")

def gen_exp_vs_map():
    print("\nGENERATOR EXPRESSIONS VS MAP")

    print("\n> list manipulation")

    print("> function case: get abs of value")

    T = tuple(range(-2,4))
    print(f"> > test tuple: {T}")

    print("> > > with map:",end=' ')
    print(list(map(abs,T)))

    print("> > > with gen:",end=' ')
    print(list(abs(x) for x in T))

    print("> non-function case: double the value")
    T = tuple(range(1,5))
    print(f"> > test tuple: {T}")

    print("> > > with map:",end=' ')
    print(list(map((lambda x : x*2),T)))

    print("> > > with gen:",end=' ')
    print(list(x*2 for x in T))

    print("\n> string manipulation - join")

    print("> function case - upper, split ','")

    S = "aaa,bbb,ccc"
    print(f"> > test string: {S}")

    print("> > > with comp:",end=' ') # creates pointless list
    J = ''.join([x.upper() for x in S.split(',')])
    print(J)

    print("> > > with gen:",end=' ')
    J = ''.join(x.upper() for x in S.split(','))
    print(J)

    print("> > > with map:",end=' ')
    J = ''.join(map(str.upper,S.split(',')))
    print(J)

    print("> non-function case: double the value")

    S = "aaa,bbb,ccc"
    print(f"> > test string: {S}")

    print("> > > with comp:",end=' ')
    J = ''.join([x*2 for x in S.split(',')])
    print(J)

    print("> > > with gen:",end=' ')
    J = ''.join(x*2 for x in S.split(','))
    print(J)

    print("> > > with map:",end=' ')
    J = ''.join(map((lambda x : x*2),S.split(',')))
    print(J)

    print("\n> nesting: double abs value")

    T = tuple(range(-2,4))
    print(f"> > test tuple: {T}")

    print("> > > with comp:",end=' ')
    print([x*2 for x in [abs(y) for y in T]])

    print("> > > with gen:",end=' ')
    print(list(x*2 for x in (abs(y) for y in T)))

    print("> > > with map",end=' ')
    print(list(map((lambda x : x*2),map(abs,T))))

    print("\n> unnested (flat) equivalents")

    T = tuple(range(-2,4))
    print(f"> > test tuple: {T}")

    print("> > > with comp:",end=' ')
    print([abs(x)*2 for x in T])

    print("> > > with gen:",end=' ')
    print(list(abs(x)*2 for x in T))

    print("> > > with map:",end=' ')
    print(list(map((lambda x : abs(x)*2),T)))

def gen_exp_vs_filter():
    print("\nGENERATOR EXPRESSIONS VS FILTER")

    print("> join words longer than 1 letter")
    
    S = 'aa bbb c'
    print(f"> > test string: {S}")

    print("> > > with gen with if:",end=' ')
    J = ''.join(x for x in S.split() if len(x)>1)
    print(J)

    print("> > > with filter and lambda:",end=' ')
    J = ''.join(list(filter((lambda x : len(x)>1),S.split())))
    print(J)

    print("\n> join (len>1), upper")

    S = 'aa bbb c'
    print(f"> > test string: {S}")

    print("> > > with gen with if:",end=' ')
    J = ''.join(x.upper() for x in S.split() if len(x)>1)
    print(J)

    print("> > > with map, filter, lambda:",end=' ')
    J = ''.join(list(map(str.upper,filter((lambda x : len(x)>1),S.split()))))
    print(J)

    print("> > > with for loop:",end=' ')
    res = ''
    for x in S.split():
        if len(x)>1:
            res += x.upper()
    print(res)

    print("> > > with for loop and gen func:",end=' ')

    def gen_sub(S):
        for x in S.split():
            if len(x)>1:
                yield x.upper()
    J = ''.join(gen_sub(S))
    print(J)

def gen_func_vs_exp():
    print("\nGENERATOR FUNCTIONS VS GENERATOR EXPRESISONS")

    S = 'spam'
    n = 4
    print(f"> repeat each function in string '{S}' {n} times")

    print("> > with gen exp, 1 by 1:")
    G = (x*4 for x in S)
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")

    print("> > with gen exp, force list:",end=' ')    
    print(list(x*4 for x in S))

    def repeat_char_n_times(n,S):
        for x in S:
            yield x*n
    
    print("> > with gen func, 1 by 1:")
    I = iter(repeat_char_n_times(n,S))
    print(f"> > > {I.__next__()}")
    print(f"> > > {I.__next__()}")
    print(f"> > > {I.__next__()}")
    print(f"> > > {I.__next__()}")

    print("> > with gen func, force list:",end=' ')
    print(list(repeat_char_n_times(n,S)))
    
def gen_single_iter():
    print("\nGENERATORS ARE SINGLE ITERATION OBJECTS")

    print("\n> iterator expressions")

    print("> gens support only one active iteration")

    S = 'SPAM'; n = 4

    print(f"> > test string: {S}, number of repeats: {n}")

    G = (c*n for c in S)

    print("> gen exps are their own iters")
    print(f"> > iter(G) is G ? {iter(G) is G}")

    print("> advance two iters in parallel:")
    I1 = iter(G); I2 = iter(G)

    print(f"I1 = {next(I1)} \t I2 = ----")
    print(f"I1 = {next(I1)} \t I2 = {next(I2)}")
    print(f"I1 = ---- \t I2 = {next(I1)}")

    print("> Iterators are exhausted after 1 iteration")
    print("> > try creating new on same gen:",end=' ')
    I3 = iter(G)
    try:
        print(f"I3 = {next(I3)}")
    except:
        print(f"error!")

    G = (c*n for c in S)
    I4 = iter(G)

    print("> create new gen and its iter, force list:")
    print(f"> > {list(I4)}")
    print(f"> iterator is exhausted, try next:",end=' ')
    try:
        print(f"fI4 = {next(I4)}")
    except:
        print(f"error!")

    print("\n> iterator functions")

    def repeat_char_n_times(S,n):
        for c in S:
            yield c*n
    
    
    G = repeat_char_n_times(S,n)

    print("> gen func are their own iters")
    print(f"> > iter(G) is G ? {iter(G) is G}")

    print("> advance two iters in parallel:")
    I1 = iter(G); I2 = iter(G)

    print(f"I1 = {next(I1)} \t I2 = ----")
    print(f"I1 = {next(I1)} \t I2 = {next(I2)}")
    print(f"I1 = ---- \t I2 = {next(I1)}")

    print("> ... everything same as for exps")

def gen_yield_from():
    print("\nYIELD FROM EXTENSION")

    print("> allows delegation to a subgenerator")
    print("> equivalent to a yielding for loop")

    n = 5
    print(f"\n> yield x**1 then x**2 in range up to {n}")

    print("> > old way - with for loops:",end=' ')
    def both_for_loop(n):
        for i in range(n): yield i
        for i in (x**2 for x in range(n)): yield i
    print(list(both_for_loop(n)))
    print(' : '.join(str(i) for i in both_for_loop(n)))

    print("> > new way - with yield from:",end=' ')
    def both_yield_from(n):
        yield from range(n)
        yield from (x**2 for x in range(n))
    print(list(both_yield_from(n)))
    print(' : '.join(str(i) for i in both_yield_from(n)))

def built_in_generation():
    print("\nGENERATION IN BUILT-IN TYPES,TOOLS,CLASSES")

    print("\n> yield from dict:")
    D = {'a':1,'b':2,'c':3}
    print(f"> > test dict: {D}")

    print("> > with for loop:")
    for k in D:
        print(f"> > > {k} => {D[k]}")

    print("> > manually:")
    Id = iter(D)
    print(f"> > > Id = {next(Id)}")
    print(f"> > > Id = {next(Id)}")
    print(f"> > > Id = {next(Id)}")

    print("\n> yield from file:")

    path = sys.path[0]
    filename = 'test.txt'
    filepath = path + "\\" + filename

    for line in open(filepath):
        print(f"> > {line.rstrip()}")

    print("\n> directory walkers:")

    print("> with for loop:")
    for (root,subs,files) in os.walk('.'):
        for name in files:
            if name.startswith('dat'):
                print(f"> > {root}, {name}")
    
    print("\n> manually:")
    G = os.walk('.')
    print(f"> > iter(G) is G ? {iter(G) is G}")
    print("> > advance the iterator:")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    print(f"> > > {G.__next__()}")
    # ...

    print("\n> generators and function application")

    print("\n> function returns 'a, b and c'")
    def f(a,b,c):
        return "%s,%s and %s" % (a,b,c)
    
    print(f"> > normal positionals: {f(0,1,2)}")
    print(f"> > unpack range val: {f(*range(3))}")
    print(f"> > unpack gen.exp.val: {f(*(i for i in range(3)))}")

    D = dict(a='Bob',b='dev',c=40.5)
    print(f"> > test dict: {D}")

    print(f"> > normal keywords: {f(a='Bob',b='dev',c=40.5)}")
    print(f"> > unpack dict: key=val: {f(**D)}")
    print(f"> > unpack keys iterator: {f(*D)}")
    print(f"> > unpack view iterator: {f(*D.values())}")

    print("\n> str.upper, add space between letters")
    
    S = 'spam'
    print(f"> > test string: {S}")

    print("> > with straight for loop:",end=' ')
    for s in S: print(s.upper(),end=' ')
    print()

    print("> > with force list and gen:",end=' ')
    list(print(s.upper(),end=' ') for s in S)
    print()

    print("> > with extended unpacking and gen:",end=' ')
    print(*(s.upper() for s in S))
    print()

def user_defined_iter_in_class():
    print("\nUSER DEFINED ITERABLES IN CLASSES")

    print("> implementing arbitrary gens with classes")

    class SomeIterable:
        def __iter__(x):
            ...
            # on iter(): return self or supplemental object
        
        def __next__(x):
            ...
            # on next(): coded here, or in another class

def gen_scrambled_seq():
    print("\nEXAMPLE: GENERATING SCRAMBLED SEQUENCES")

    print("> basic sequence reordering with slicing:")
    
    L = [1,2,3]
    print(f"> > test list: {L}")
    S = 'spam'
    print(f"> > test string: {S}")

    print("\n> classical approach")

    print("> with straight for:")
    Ltemp = L[:]
    res = []
    for i in range(len(L)):
        res.append(Ltemp)
        Ltemp = Ltemp[1:] + Ltemp[:1]
    print(f"> > {res}")
    
    Stemp = S
    res = []
    for i in range(len(S)):
        res.append(Stemp)
        Stemp = Stemp[1:] + Stemp[:1]
    print(f"> > {res}")

    print("> with for and def:")

    def roll_for(seq):
        res = []
        for i in range(len(seq)):
            res.append(seq[i:]+seq[:i])            
        return res
    
    print(f"> > {roll_for(L)}")
    print(f"> > {roll_for(S)}")

    print("> with comp and def:")

    def roll_comp(seq):
        return [seq[i:]+seq[:i] for i in range(len(seq))]

    print(f"> > {roll_comp(L)}")
    print(f"> > {roll_comp(S)}")

    print("\n> generator functions")

    def roll_gen(seq):
        for i in range(len(seq)):
            yield seq[i:]+seq[:i]
    
    print(f"> > {list(roll_gen(L))}")
    print(f"> > {list(roll_gen(S))}")

    print("> yield 1 by 1:")
    
    print("> >",end=' ')
    for l in roll_gen(L): print(l,end=' : ')
    print()
    print("> >",end=' ')
    for s in roll_gen(S): print(s,end=' : ')
    print()

    print("\n> generator expressions")

    Gl = (L[i:]+L[:i] for i in range(len(L)))
    print(f"> > {list(Gl)}")
    Gs = (S[i:]+S[:i] for i in range(len(S)))
    print(f"> > {list(Gs)}")

    print("> yield 1 by 1:")
    # need to restart the generator
    Gl = (L[i:]+L[:i] for i in range(len(L)))
    Gs = (S[i:]+S[:i] for i in range(len(S)))

    print("> >",end=' ')
    for l in Gl: print(l,end=' : ')
    print()
    print("> >",end=' ')
    for s in Gs: print(s,end=' : ')
    print()

    print("\n> lambdas with generators")

    G = lambda seq : (seq[i:]+seq[:i] for i in range(len(seq)))

    print(f"> > {list(G(L))}")
    print(f"> > {list(G(S))}")

    print("> yield 1 by 1:")

    print("> > ",end=' ')
    for g in G(L): print(g,end=' : ')
    print()

    print("> >",end=' ')
    for g in G(S): print(g,end=' : ')
    print()

def generalized_gen_functions():
    print("\nGENERALIZED GEN FUNCTIONS")

    def intersect(first,*rest):
        res=[]
        for x in first:
            if x in res: continue
            for seq in rest:
                if x not in seq: break
            else:
                res.append(x)
        return res

    def union(*args):
        res = []
        for seq in args:
            for x in seq:
                if x not in res:
                    res.append(x)
        return res

    roll_gen = lambda seq : (seq[i:]+seq[:i] for i in range(len(seq)))

    def tester(func,items,trace=True):
        for seq in roll_gen(items):
            if trace: print(f"\n> test list: {seq}")
            print(f"> > {func.__name__}: {func(*seq)}")

    L=[[1,2,3],[2,3,4],[3,4,5]]
    S=['SPAM','SCAM','SLAM','FLAM','PRAM']
    
    print("\n> INTERSECT")
    tester(intersect,L)
    tester(intersect,S)

    print("\n> UNION")
    tester(union,L)    
    tester(union,S)    

def permute_list(seq):
    if not seq:                             # if no sequence
        return [seq]                        # return empty sequence
    else:
        res=[]
        for i in range(len(seq)):
            rest = seq[:i]+seq[i+1:]        # delete current node
            for x in permute_list(rest):    # permute the others
                res.append(seq[i:i+1]+x)    # add node at front
        return res

def permute_gen(seq):
    if not seq:
        yield seq
    else:
        for i in range(len(seq)):
            rest = seq[:i]+seq[i+1:]
            for x in permute_gen(rest):
                yield seq[i:i+1]+x

def permute_test(seq):
    if len(seq)<=1:
        yield seq
    else:
        for i,f in enumerate(seq):
            rest = seq[:i]+seq[i+1:]
            for p in permute_test(rest):
                yield [f]+p

def permutations():
    print("\nEXAMPLE: ALL PERMUTATIONS OF A SEQUENCE")

    print("> set of all possible orderings")

    L = [1,2,3]
    print(f"> > test list: {L}")
    S = 'spam'
    print(f"> > test string: {S}")

    print("> permutations: list")
    print(permute_list(L))
    print(permute_list(S))
    print("> permutations: gen")
    print(list(permute_gen(L)))
    print(list(permute_gen(S)))

def gen_use():
    print("\nGOOD USE OF GENERATORS")

    print("> responsiveness in large sets")

    L = [1,2,3]
    print(f"> > test list: {L}")
    print("> with force list:")
    for x in permute_list(L): print(x)
    print()
    print("> with generator:")
    for x in permute_gen(L): print(x)

    print("> yielding from large sets")
    import math
    n = 20
    print(f"> > permutations of a set of {n} elements: {math.factorial(n)}")
    
    seq = list(range(n))
    import random
    random.shuffle(seq)
    p = permute_gen(seq)
    print("> > > random shuffle")
    print(f"> > > advance: {next(p)}")
    print(f"> > > advance: {next(p)}")
    random.shuffle(seq)
    p = permute_gen(seq)
    print("> > > random shuffle")
    print(f"> > > advance: {next(p)}")
    print(f"> > > advance: {next(p)}")

def emulating_zip_map():
    print("\nEMULATING ZIP AND MAP WITH ITERATION TOOLS")

    L = list(range(-2,3))
    S1 = 'abc'
    S2 = 'xyz123'

    L1 = list(range(1,4))
    L2 = list(range(5,10))

    print("> zip pairs items from iterables:")
    print(f"> > 1-sequence: {list(zip(L))}")
    print(f"> > 2-sequence: {list(zip(S1,S2))}")

    print("> map passes paired items to function:")
    print(f"> > 1-sequence, abs: {list(map(abs,L))}")
    print(f"> > 2-sequence, pow: {list(map(pow,[1,2,3],[2,3,4]))}")

    print(f"> accept arbitrary iterables: {L1}, {L2}")
    print(f"> > zip, x+y: {[x+y for (x,y) in zip(L1,L2)]}")
    print(f"> > map, x+y: {list(map((lambda x,y:x+y),L1,L2))}")

    print("\n> coding your own map function")

    print("> > with force list")

    def my_map_list(func,*seqs):
        res = []
        for line in zip(*seqs):
            res.append(func(*line))
        return res

    print(f"> > > 1-sequence, abs: {my_map_list(abs,L)}")
    print(f"> > > 2-sequence, pow: {my_map_list(pow,L1,L2)}")
    
    print("> > with list comp")

    def my_map_comp(func,*seqs):
        return [func(*line) for line in zip(*seqs)]

    print(f"> > > 1-sequence, abs: {my_map_comp(abs,L)}")
    print(f"> > > 2-sequence, pow: {my_map_comp(pow,L1,L2)}")

    print("> > with gen func")

    def my_map_gen_func(func,*seqs):
        for line in zip(*seqs):
            yield func(*line)

    print(f"> > > 1-sequence, abs: {list(my_map_gen_func(abs,L))}")
    print(f"> > > 2-sequence, pow: {list(my_map_gen_func(pow,L1,L2))}")

    print("> > with gen exp")

    def my_map_gen_exp(func,*seqs):
        return (func(*line) for line in zip(*seqs))

    print(f"> > > 1-sequence, abs: {list(my_map_gen_exp(abs,L))}")
    print(f"> > > 2-sequence, pow: {list(my_map_gen_exp(pow,L1,L2))}")

    print("> > 2.X-style map with pad")

    def my_map_with_pad(func,*seqs,pad=None):
        seqs = [list(S) for S in seqs]
        res = []
        while any(seqs):
            line = tuple((S.pop(0) if S else pad) for S in seqs)
            res.append(func(*line) if all(line) else pad)
        return res
    
    print(f"> > > 1-sequence, abs: {list(my_map_with_pad(abs,L))}")
    print(f"> > > 2-sequence, pow: {list(my_map_with_pad(pow,L1,L2))}")

    print("> > alt. imp. with max. length list")

    def my_map_alt_list(func,*seqs,pad=None):
        max_len = max(len(S) for S in seqs)
        while any(seqs):
            L = [tuple((S[i] if len(S)>i else pad) for S in seqs) for i in range(max_len)]            
            return [(func(*line) if all(line) else pad) for line in L]

    print(f"> > > 1-sequence, abs: {list(my_map_alt_list(abs,L))}")
    print(f"> > > 2-sequence, pow: {list(my_map_alt_list(pow,L1,L2))}")

    print("> > alt. imp. with max. length gen")

    def my_map_alt_for(func,*seqs,pad=None):
        for i in range(max(len(S) for S in seqs)):
            line = []
            for S in seqs:                    
                line.append(S[i] if len(S)>i else pad)
            yield func(*line) if all(line) else pad

    print(f"> > > 1-sequence, abs: {list(my_map_alt_for(abs,L))}")
    print(f"> > > 2-sequence, pow: {list(my_map_alt_for(pow,L1,L2))}")

    print("\n> coding your own zip function")

    print("> > with force list")

    def my_zip_list(*seqs):
        seqs = [list(S) for S in seqs]
        res = []
        while all(seqs):
            res.append(tuple(S.pop(0) for S in seqs))
        return res    

    print(f"> > > {my_zip_list(L1,L2)}")

    print("> > with gen func")

    def my_zip_gen(*seqs):
        seqs = [list(S) for S in seqs]
        while all(seqs):
            yield tuple(S.pop(0) for S in seqs)
        
    print(f"> > > {list(my_zip_gen(L1,L2))}")

    print("> > alt. imp. with min. length")

    print("> > > with force list")

    def my_zip_alt_list(*seqs):
        min_len = min(len(S) for S in seqs)
        return [tuple(S[i] for S in seqs) for i in range(min_len)]

    print(f"> > > > {my_zip_alt_list(L1,L2)}")

    print("> > > with gen func")        

    def my_zip_alt_gen(*seqs):
        min_len = min(len(S) for S in seqs)
        return (tuple(S[i] for S in seqs) for i in range(min_len))

    print(f"> > > > {list(my_zip_alt_gen(L1,L2))}")

    print("> > alt. imp. with iters and next")

    def my_zip_alt_iters(*seqs,pad=None,type=all):
        iters = list(map(iter,seqs))
        while iters:
            res=[]
            for i in iters:
                try:
                    res.append(next(i))
                except:
                    res.append(pad)
            if type(res):
                yield tuple(res)
            else:
                return

    print(f"> > > {list(my_zip_alt_iters(L1,L2,type=all))}")
