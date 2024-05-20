def constructors_expressions():
    print("\n__init__ and ...")

    class Number:
        def __init__(self,start):
            self.data = start

        def __add__(self,other):                # on inst + other
            return Number(self.data + other)
        
        def __sub__(self,other):                # on inst + other
            return Number(self.data - other)
    
    x = Number(5)
    print(f"x initialized to {x.data}")
    y = x + 2
    print(f"add 2 to x to get y. y = {y.data}")
    z = x - 2
    print(f"subtract 2 from x to get z. z = {z.data}")

def common_o_o_methods():
    print("\nCommon operator overloading methods")

    # __init__            # object creation: x = Class(args)
    # __new__             # object creation before __init__
    # __call__            # f.calls, x(*pargs,**kargs)
    # __bool__            # bool(x), truth tests
    # __len__             # len(x)
    # __del__             # object reclamation of x
    # __add__             # x + y, x += y (if no __iadd__)
    # __iadd__            # x += y (or else add)
    # __or__              # x | y, x |= y (if no __ior__)
    # __ior__             # x |= y (or else or)
    # __repr__,__str__    # print(x),repr(x),str(x)
    # __getattr__         # x.undefined
    # __setattr__         # x.any = value
    # __delattr__         # del x.any
    # __get__,            # x.attr
    # __set__,            # x.attr=value
    # __delete__          # del x.attr
    # __getitem__         # x[key],x[i:j], for loops
    # __setitem__         # x[key]=value, x[i:j]=iterable
    # __delitem__         # del x[key], del x[i:j]
    # __lt__,__gt__,      # x < y, x > y
    # __le__,__ge__,      # x <= y, x >= y
    # __eq__,__ne__       # x == y, x != y
    # __iter__,__next__   # I=iter(x),next(I); loops,comps,...
    # __contains__        # item in x (any iterable)
    # __index__           # int. value; hex(x),bin(x),oct(x),...
    # __enter__,__exit__  # with obj as var

def speed_comparison():
    print("\nlen vs. __len__ speed")
    
    import timeit

    ss = "L=list(range(100))"
    s1 = "x = len(L)"
    s2 = "x = L.__len__()"

    n = 1000000
    r = 10

    print(f"> {ss}")
    
    t1 = min(timeit.repeat(setup=ss,stmt=s1,number=n,repeat=r))
    print(f"> {s1}")
    print(f"> > best of {r}x total of {n} runs: {t1:.6f}")

    t2 = min(timeit.repeat(setup=ss,stmt=s2,number=n,repeat=r))
    print(f"> {s2}")
    print(f"> > best of {r}x total of {n} runs: {t2:.6f}")

def indexing_slicing():
    print("\nINDEXING AND SLICING")

    class Indexer:
        def __getitem__(self,index):
            return index**2     # on indexing return square of the index

    x = Indexer()
    print(f"> call x[2], get square of the index: {x[2]}")

    print(f"> loop through first 5 indices:", end=' ')
    for i in range(5):
        print(x[i], end=' ')

def intercepting_slices():
    print("\nSLICING REFRESHER")

    print("\n> slice with slice syntax:")
    L = [5,6,7,8,9]
    print(f"> test list: {L}")
    print(f"> L[2:4]: {L[2:4]}")
    print(f"> L[1:]: {L[1:]}")
    print(f"> L[:-1]: {L[:-1]}")
    print(f"> L[::2]: {L[::2]}")

    print("\n> actually slice calls > indexing")
    print(f"> test list: {L}")
    print(f"> L[2:4]: {L[slice(2,4)]}")
    print(f"> L[1:]: {L[slice(1,None)]}")
    print(f"> L[:-1]: {L[slice(None,-1)]}")
    print(f"> L[::2]: {L[slice(None,None,2)]}")

    class Indexer:
        data = [5,6,7,8,9]
        def __getitem__(self,index):
            print('getitem:',index)
            return self.data[index]
    
    x = Indexer()
    print("\n> get indicies, customized:")
    print(f"value: {x[0]}")            # call __getitem__ with index 0
    print(f"value: {x[1]}")            # call __getitem__ with index 1
    print(f"value: {x[-1]}")           # call __getitem__ with index -1

    print("\n> get slices, customized:")
    print(f"> x[2:4]: {x[2:4]}")
    print(f"> x[1:]: {x[1:]}")
    print(f"> x[:-1]: {x[:-1]}")
    print(f"> x[::2]: {x[::2]}")

    class Indexer:
        def __getitem__(self,index):
            if isinstance(index,int):
                print('indexing',index)
            else:
                print('slicing',index.start,index.stop,index.step)
    
    x = Indexer()
    print("\n> get indicies and slices:")
    print(f"> x[99]: {x[99]}")
    print(f"> x[1:99:2]: {x[1:99:2]}")
    print(f"> x[1:]: {x[1:]}")

    class IndexSetter:
        def __init__(self):
            self.data = []

        def __setitem__(self,index,value):  # intercept index or slice asignment
            print('setitem',index,value)
            self.data[index]=value          # assign index or slice
    
    print("\n> set indicies and slices to values:")
    x = IndexSetter()
    x[0:2]=(0,1,2)
    print(f"> x data: {x.data}")

def index_o_o():
    print("\n__index__ IS NOT INDEXING")

    # this method terutns an integer value for an instance
    # used by built-ins that convert to digit strings

    class C:
        def __index__(self):
            return 255
        
    x = C()
    print(f"> int value of hex(x) (255): {hex(x)}")
    print(f"> int value of oct(x) (255): {oct(x)}")
    print(f"> int value of bin(x) (255): {bin(x)}")

def index_iteration():
    print("\n INDEX ITERATION: __getitem__")

    class StepperIndex:
        def __init__(self,value=''):
            self.data = ''
        
        def __getitem__(self,i):
            return self.data[i]
    
    x = StepperIndex()
    print(x)
    x.data = 'spam'
    print("> set x data value to 'spam'")
    print("> loop through x data:",end=' ')
    for item in x:
        print(item,end=' ')
    print("\n> all iteration contexts are supported")
    print(f"> mem. test: p in spam? {'p' in x}")
    print(f"> list comp: {[c for c in x]}")
    print(f"> map call: {list(map(str.upper,x))}")
    (a,b,c,d) = x
    print(f"> sequence assign: a={a},b={b},c={c},d={d}")
    print(f"> list convert: {list(x)}")
    print(f"> tuple convert: {tuple(x)}")
    print(f"> str join: {'.'.join(x)}")

def iterable_objects():
    # iteration protocol (__iter__ method) preferred to __getitem__

    class Squares:
        def __init__(self,start,stop):
            self.value = start-1
            self.stop = stop
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.value == self.stop:
                raise StopIteration
            self.value += 1
            return self.value ** 2
    
    print("> iterate through (1...5):",end=' ')
    for i in Squares(1,5):          # for calls iter, which calls __iter__
        print(i, end=' ')           # each iteration calls __next__
    
    print("\n> iterate manually:")
    x = Squares(1,5)
    I = iter(x)
    print(f"> next: {next(I)}")
    print(f"> next: {next(I)}")
    print(f"> next: {next(I)}")
    print(f"> next: {next(I)}")
    print(f"> next: {next(I)}")

    # __iter__ is designed for iteration, not random indexing
    # they don't overload the indexing expression at all
    # you can collect their items in a sequence such as list

    print("\n> try to index:")
    try:
        print(f"> x[1]: {x[1]}")
    except Exception as e:
        print(f"> error! {e}")
        
    print("\n> squares class - designed as one-shot iteration")
    print("> > make an iterable with state:")
    X = Squares(1,5)
    print(f"> > use the iterable in comp: {[n for n in X]}")
    print(f"> > now it is exhausted (try same comp): {[n for n in X]}")
    print(f"> > make a new iterable object (direct comp): {[n for n in Squares(1,5)]}")
    print(f"> > or directly convert to list (same comp): {list(Squares(1,5))}")
    print(f"> > > converting to list enables multiple scans (of the list) > memory!")
    print(f"> > each test exhausts the iterable: 36 in (Squares(1,5))? {36 in Squares(1,5)}")
    print("> > tuple assign, each calls iter then next, ",end='')
    a,b,c = Squares(1,3)
    print(f"a = {a}, b = {b}, c = {c}")
    X = Squares(1,5)
    print(f"> > tuple convert, each exhausts the iterable: {tuple(X)}, {tuple(X)}")
    X = list(Squares(1,5))
    print(f"> > tuple convert multiple, can if converted to list: {tuple(X)}, {tuple(X)}")
    X = ':'.join(map(str,Squares(1,5)))
    print(f"> > any iteration context applies, i.e. join using ':': {X}")

def classes_vs_gens():
    print("\nCLASSES VS GENERATORS")

    def gen_squares(start,stop):
        for x in range(start,stop+1):            
            yield x**2

    print("> generators automatically produce iterable objects: ",end='')
    for x in gen_squares(1,5):
        print(x,end=' ')

    print("\n> this example can be coded directly: ",end='')
    for x in (s**2 for s in range(1,6)):
        print(x,end=' ')

    print(f"\n> using comp for conciseness: {[x**2 for x in range(1,6)]}")

    print("> but classes are more explicit and provide extra features")

    print("> we can combine __iter__ + yield for generators")

    G = gen_squares(1,5)    # create a gen with __iter__ and __next__
    print(f"> gen == its iter? {G == G.__iter__()}")
    print(f"> convert to list auto runs iter and next: {list(gen_squares(1,5))}")

    print("> if gen.func. with yield is a method called __iter__")
    print("> > whenever invoked it will return a new gen. with next")
    
    class SquaresGen:
        def __init__(self,start,stop):
            self.start = start
            self.stop = stop
        
        def __iter__(self):
            for value in range(self.start,self.stop+1):
                yield value**2
    
    print("> iterate through values:",end=' ')
    for x in SquaresGen(1,5):
        print(x,end=' ')
    print()

    print("> generate values manually:",end=' ')
    S = SquaresGen(1,5) # runs __init__ saves inst. state
    I = iter(S)         # runs __iter__ returns generator
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    # print(next(I),end=' ')        # raises StopIteration
    print()

    class SquaresGenAlt(SquaresGen):
        def gen(self):
            for value in range(self.start,self.stop+1):
                yield value**2
        def __iter__(self):
            self.gen()
    
    print("> > using __iter__ skips manual attr. fetch and call stop")
    print("> generate values manually:",end=' ')
    S = SquaresGenAlt(1,5)  # runs super init
    I = iter(S.gen())       # call gen. manually for iterable/iterator
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    print(next(I),end=' ')
    # print(next(I),end=' ')        # raises StopIteration
    print()

def multi_iters_one_object():
    print("\nMULTIPLE ITERATIONS IN ONE OBJECT")

    def dbl_loop(S):
        for x in S:
            for y in S:
                print(x+y, end=' ')
        print()

    def dbl_loop_join(S):
        for x in S:
            for y in S:
                print(f"{x}:{y}",end=' ')
        print()

    print("> example: nested for loop, combs of 'ace':")
    S = 'ace'
    dbl_loop(S)
    
    import skipper as sp

    print("> class with supplemental class for iteration")
    print("> supports multi loops directly - each call new iterator")
    
    S = 'abcdef'
    print(f"> example: nested for loop, combs of {S} + skip every other ")
    
    X = sp.SkipObject(S)
    dbl_loop(X)

    print("> instead of classes, we can use slicing:")
    dbl_loop(S[::2])

    print("> not the same (stores res in memory + creates new objects)")

    print("> with yield we get multi scan automatically")
    print("> each call to iter creates a new generator")

    X = sp.SkipYield(S)
    dbl_loop(X)
    
    class SquaresGen:
        def __init__(self,start,stop):
            self.start = start
            self.stop = stop
        
        def __iter__(self):
            for value in range(self.start,self.stop+1):
                yield value**2
    
    print("> multi scan with yield:",end=' ')
    S = SquaresGen(1,3)
    dbl_loop_join(S)

    print("> without yield requires supplemental iterator class")

    class SquaresNonGen:
        def __init__(self,start,stop):
            self.start = start
            self.stop = stop
        
        def __iter__(self):
            return SquaresIterator(self.start,self.stop)

    class SquaresIterator:
        def __init__(self,start,stop):
            self.value = start -1
            self.stop = stop
        def __next__(self):
            if self.value == self.stop:
                raise StopIteration
            self.value += 1
            return self.value**2
    
    print("> multi scan without yield",end=' ')
    S = SquaresNonGen(1,3)
    dbl_loop_join(S)

    print("> manual multi scan:")
    S = SquaresNonGen(1,3)
    I = iter(S)
    J = iter(S)
    print(next(I),':',next(J),sep='',end=' ')
    print(next(I),':',next(J),sep='',end=' ')
    print(next(I),':',next(J),sep='',end=' ')
    print()

def membership_testing():
    print("\nMEMBERSHIP TESTING")

    import contains as ct

    A = ct.Iters('spam')
    B = ct.ItersYield('spam')

    for X in (A,B):
        print(f"> test string: {X}")
        print(f"> X[0]: {X[0]}")
        print(f"> X[1:]: {X[1:]}")
        print(f"> X[slice]: {X[slice(1,None)]}")
        print(f"> list: {list(X)}")

def attribute_access():
    print("INTERCEPTING ATTRIBUTE ACCESS")

    print("getattr")
    class Empty:
        def __getattr__(self,attr):     # on self.undefined
            if attr == 'age':
                return 40
            else:
                raise AttributeError(attr)
    
    X = Empty()
    print(f"> fetching undefined attributes:")
    print(f"> 'age': {X.age}")
    try:
        print(f"> 'name': {X.name}")
    except AttributeError as e:
        print(f"> error! attribute '{e}' is undefined")

    print("setattr")
    class AccessControl:
        def __setattr__(self,attr,value):
            if attr == 'age':
                self.__dict__[attr] = value + 10
                # object.__setattr__(self,attr,value+10)    # also works
                # self.age = value + 10         # triggers infinite loop
                # setattr(self,attr,value+10)   # triggers infinite loop
            else:
                raise AttributeError(f"attribute '{attr}' is not allowed")
    
    X = AccessControl()
    print(f"> assign attributes:")
    X.age = 40
    print(f"> 'age': {X.age}")
    try:
        X.name = 'Bob'
        print(f"> 'name': {X.name}")
    except AttributeError as e:
        print(f"> error! {e}")

    print("delattr")
    class Cleaner:
        def __init__(self,age=40,name='Bob'):
            self.age = age
            self.name = name
        def __delattr__(self,attr):
            if attr == 'age':                
                del self.__dict__[attr]
            elif attr == 'name':
                raise AttributeError(f"cannot delete attribute '{attr}'")
    
    X = Cleaner()
    print(f"> cleaner initialized with defaults:")
    del X.age
    print("> deleted attribute 'age'")
    try:
        del X.name
        print("> deleted attribute 'name'")
    except AttributeError as e:
        print(f"> error! {e}")

def emulating_privacy():
    print("\nEMULATING PRIVACY FOR INSTANCE ATTRIBUTES")

    print("> allow subclass to have a list of private names")
    print("> these names cannot be assigned as instance attributes")

    class PrivateExc(Exception): pass

    class Privacy:
        def __setattr__(self,attrname,value):       # on self.attrname = value
            if attrname in self.privates:
                raise PrivateExc(attrname,self)     # make, raise user-def. exc.
            else:
                self.__dict__[attrname] = value
    
    class Test1(Privacy):
        privates = ['age']
    
    class Test2(Privacy):
        privates = ['name','pay']

        def __init__(self,attr,value):
            # self.__dict__[attr] = value           # init without setattr
            setattr(self,attr,value)
    
    print("\nTest1 - init")
    x = Test1()
    print("> initialized with defaults")
    print("Test1 - assign")
    x.name = 'Bob'
    print("> inst. attr. 'name' set to 'Bob'")
    print("> attempt to assign attr 'age'")
    try:
        x.age = 40
        print("> inst. attr. 'age' set to 40")
    except Exception as e:
        print(f"> error! attr '{e.args[0]}' is private!")

    print("\nTest2 - init")
    y = Test2('age',40)
    print("> initialized with 'age'=40")
    print("> attempt to assign attr 'name'")
    try:
        y.name = 'Bob'
        print("> inst. attr. 'name' set to 'Bob'")
    except Exception as e:
        print(f"> error! attr '{e.args[0]}' is private!")

    print("Test2 - assign")
    print("> attempt to assign attr 'name'")
    try:
        y = Test2('name','Bob')
        print("> initialized with 'name'='Bob'")
    except Exception as e:
        print(f"> error! attr '{e.args[0]}' is private!")

def string_repr():
    print("\nSTRING REPRESENTATION")

    print("> object which adds two numbers")
    print()

    class Adder:
        def __init__(self, value=0):
            self.data = value           # initialize data
        def __add__(self,other):
            self.data += other          # add other in-place (bad form)
                                        # should return Adder(self.data+other)
                                        # then can assign Y = X + 1
    
    X = Adder(2)
    print(f"> > default display (print): {X}")
    X+1
    print(f"> > default display (print): {X}")
    print(repr("> > default display (repr): " + str(X)))
    print()

    class AdderRepr(Adder):
        # customizing display with __repr__ method
        def __repr__(self):
            return f"AdderRepr({self.data})"
    
    X = AdderRepr(2)
    print(f"> > with __repr__ method: {X}")
    X+1                                         # < this is why iadd is bad form
    print(f"> > with __repr__ method: {X}")     # < retains new value (init+1)
    S = str(X)
    print(f"> > converted to string: {S}")
    S = repr(X)
    print(f"> > evaluated repr: {S}")
    print()

    class AdderStr(Adder):
        def __str__(self):
            return f"[Value: {self.data}]"
    
    X = AdderStr(2)
    print(f"> > with __str__ method: {X}")
    X+1
    print(f"> > with __str__ method: {X}")
    S = str(X)
    print(f"> > converted to string: {S}")
    S = repr(X)
    print(f"> > repr evals to default: {S}")
    print()

    # __repr__ if single display for all contexts
    # if both: __repr__ for low-level, __str__ for end-user
    # __str__ overrides __repr__ for user-frinedly

    class AdderBoth(Adder):
        def __str__(self):
            return f"[Value: {self.data}]"      # user-friendly
        def __repr__(self):
            return f"AdderBoth({self.data})"    # as-code string
    
    X = AdderBoth(2)
    print(f"> > with __str__ method: {X}")
    X+1
    print(f"> > with __str__ method: {X}")
    S = str(X)
    print(f"> > with __str__ method: {S}")
    S = repr(X)
    print(f"> > evaluated repr: {S}")
    print()

    print("> __str__ vs __repr__ in various contexts")

    # __str__ might only apply when objects appear at the top level of print op
    # objects nested in larger objects might still print with their __repr__

    class PrinterStr:
        def __init__(self, value):
            self.value = value
        def __str__(self):                  # used for instance itself
            return str(self.value)          # convert to a string res
        
    # to ensure custom display in all contexts, code __repr__

    class PrinterRepr:
        def __init__(self,value):
            self.value = value
        def __repr__(self):
            return str(self.value)

    Ls = [PrinterStr(2),PrinterStr(3)]
    Lr = [PrinterRepr(2),PrinterRepr(3)]

    for L in (Ls,Lr):
        print("> __str__ runs when instance printed: ",end='')
        for x in L:
            print(x,end=' | ')
        print()

        print("> __repr__ runs when instance in list: ")
        print(L)
        print()

def right_side():
    print("\nEXTENDING BINARY OPS: RIGHT SIDE")

    print("> object which adds two numbers")

    class Adder:
        def __init__(self,value=0):
            self.data = value
        def __add__(self,other):
            print(f"(add) {self.data} + {other} = ",end='')
            return self.data + other
        def __repr__(self):
            return f"[Value: {self.data}]"
    
    X = Adder(88)
    print(f"\nclass type: {X.__class__.__name__}")
    print('-'*60)
    print(f"> initialize X to 2: {X}")
    print(f"> add 1 from right:"); print(X+1)    
    try:
        print(f"> add 1 from left:"); print(1+X)
    except Exception as e:
        print(f"> error! {e}")
    print("> supports only addition with object on the left")
    
    def add_test(ClassType):
        print(f"\nclass type: {ClassType.__name__}")
        print('-'*60)
        X = ClassType(88)
        print(f"> initialize X to 88: {X}")
        print(f"> add 1 from right: "); print(X+1)
        print(f"> add 1 from left: "); print(1+X)
        Y = ClassType(99)
        print(f"> initialize Y to 99: {Y}")
        print(f"> add X and Y: "); print(X+Y)

    # right side addition must be coded separately
    class Commuter1(Adder):
        def __radd__(self,other):
            print(f"(radd) {other} + {self.data} = ",end='')
            return other + self.data   

    # for commutative ops without special casting reuse add for radd

    # directly: calling add from radd
    class Commuter2(Adder):
        def __radd__(self,other):
            return self.__add__(other)

    # indirectly: swapping order and re-adding to trigger add
    class Commuter3(Adder):
        def __radd__(self,other):
            return self+other

    # assigning radd to be an alias for add at the top level
    class Commuter4(Adder):
        __radd__ = Adder.__add__

    # if class type needs to be propagated in results

    # type testing required to tell whether it's safe to convert
    class Commuter5(Adder):
        def __add__(self,other):
            if isinstance(other,Commuter5):         # type test to avoid nesting
                other = other.data
            return Commuter5(self.data + other)     # else + result is another C
        def __radd__(self,other):
            return Commuter5(other + self.data)

    class Commuter6(Adder):
        # without type testing results in pointless recursion and constructor calls
        def __add__(self,other):
            return Commuter6(self.data + other)
        def __radd__(self,other):
            return Commuter6(other + self.data)

    for ClassType in (Commuter1,Commuter2,Commuter3,Commuter4,Commuter5,Commuter6):
        add_test(ClassType)

def in_place():
    print("\nEXTENDING BINARY OPS: IN-PLACE")

    print("> object which adds two numbers")

    class AdderInPlace:
        def __init__(self,value=0):
            self.data = value
        def __iadd__(self,other):
            print(f"(in-place add) {self.data} + {other} = ",end='')
            self.data += other
            return self             # usually returns self
        def __repr__(self):
            return f"[Value: {self.data}]"
    
    X = AdderInPlace(2)
    print(f"\nclass type: {X.__class__.__name__}")
    print('-'*60)
    print(f"> initialize X to 2: {X}")
    print(f"> add 1 in place: ")
    X += 1
    print(X)

    Y = AdderInPlace([1])
    print(f"\nclass type: {Y.__class__.__name__}")
    print('-'*60)
    print(f"> initialize Y to [1]: {Y}")
    print(f"> add [2] to list: ")
    Y += [2]
    print(Y)
    print(f"> add [3] to list: ")
    Y += [3]
    print(Y)

    class AdderFallback:
        def __init__(self,value=0):
            self.data = value
        def __add__(self,other):
            print(f"(add) {self.data} + {other} = ",end='')            
            return AdderFallback(self.data+other)   # propagates class type
        def __repr__(self):
            return f"[Value: {self.data}]"

    Z = AdderFallback(2)
    print(f"\nclass type: {Z.__class__.__name__}")
    print('-'*60)
    print(f"> initialize Z to 2: {Z}")
    print(f"> add 1 in place: ")
    Z += 1
    print(Z)

    W = AdderFallback([1])
    print(f"\nclass type: {W.__class__.__name__}")
    print('-'*60)
    print(f"> initialize W to [1]: {W}")
    print(f"> add [2] to list: ")
    W += [2]
    print(W)
    print(f"> add [3] to list: ")
    W += [3]
    print(W)

def call_exp():
    print("\nCALL EXPRESSIONS")

    # __call__ called for function call exp. applied to instances
    # passing along whatever args were sent (supports all passing modes)

    class Callee1:
        def __call__(self,*pargs,**kargs):          # intercept instance calls
            print(f"\n> Called: {self.__class__.__name__}")
            print(f"> > Pargs: {pargs}")
            print(f"> > Kargs: {kargs}")
    
    C = Callee1()        # C is a callable object
    C(1,2,3,4)
    C(1,2)
    C(1,2,c=4,d=5)

    class Callee2:
        def __call__(self,a,b,c=5,d=6):
            print(f"\n> Called: {self.__class__.__name__}")
            print(f"> > Pargs: {a,b}")
            print(f"> > Kargs: {c,d}")
    
    C = Callee2()
    C(1,2,3,4)
    C(1,2)
    C(1,2,c=3,d=4)

    # intercepting call exp allows instances to look more like functions
    # but also retain state information for use during calls

    class Prod:
        def __init__(self, value):
            self.data = value
    
    class ProdCall(Prod):
        def __call__(self,other):
            return self.data*other
    
    print("> object which multiplies passed number with init value")

    print("\n> initialize X to 2 (call o.o.)")
    X = ProdCall(2)
    print(f"> multiply init (2) with 3: {X(3)}")
    print(f"> multiply init (2) with 4: {X(4)}")

    # same functionality can be achieved using simple methods without o.o.

    class ProdSimple(Prod):
        def comp(self,other):
            return self.data*other
    
    print("\n> initialize X to 2 (simple method)")
    X = ProdSimple(2)
    print(f"> multiply init (2) with 3: {X.comp(3)}")
    print(f"> multiply init (2) with 4: {X.comp(4)}")

    # call becomes useful when interfacing with APIs which expect functions

def callbacks():
    print("\nFUNCTION INTERFACES AND CALLBACK-BASED CODE")

    print("> stateful function objects (retain state a inst. attr.)")

    print("1) classes with __call__")

    class CallbackCall:
        def __init__(self,color):
            self.color = color
        def __call__(self):
            print(f"> turn {self.color}")
        
    # register handlers:
    cb1 = CallbackCall('blue')
    cb2 = CallbackCall('green')
    # events:    
    cb1()       # prints 'turn blue'
    cb2()       # prints 'turn green'

    # # i.e: tkinter allows to register functions as event handlers (callbacks)    
    # import tkinter as tk
    # # register handlers:
    # B1 = tk.Button(command=cb1)
    # B2 = tk.Button(command=cb2)

    print("2) closure equivalent")

    def callback_closure(color):
        def oncall():
            print(f"> turn {color}")
        return oncall
    
    # register handlers:
    cb3 = callback_closure('yellow')
    cb4 = callback_closure('red')
    # events:
    cb3()       # prints 'turn yellow'
    cb4()       # prints 'turn red'

    print("3) lambda with default equivalent")
    # register handlers:
    cb5 = (lambda color='purple': f"> turn {color}")
    cb6 = (lambda color='orange': f"> turn {color}")
    # events:
    print(cb5())       # prints 'turn purple'
    print(cb6())       # prints 'turn orange'

    print("4) bound function equivalent")

    class CallbackBound:
        def __init__(self,color):
            self.color = color
        def change_color(self):
            print(f"> turn {self.color}")

    # instantiate callbacks
    cb7 = CallbackBound('brown')
    cb8 = CallbackBound('pink')
    # register handlers:
    cb7_turn = cb7.change_color
    cb8_turn = cb8.change_color
    # events:
    cb7_turn()
    cb8_turn()

def comparisons():
    print("\nCOMPARISONS")

    print("lt: < | gt: > | le: <= | ge: >= | eq: == | ne: !=")
    print("no right-side variants, the reflected method is used")
    print("no implicit relationships, all needed should be defined")

    comps = ['<','>','<=','>=','==','!=']
        
    def compare_test_single(X,Y,comp_type):
        import operator as op
        switch = {comps[0]: op.lt,
                  comps[1]: op.gt,
                  comps[2]: op.le,
                  comps[3]: op.ge,
                  comps[4]: op.eq,
                  comps[5]: op.ne}[comp_type]

        print(f"{X} {comp_type} {Y} ? ",end='')
        try:
            print(switch(X,Y))
        except:
            print(f"error! '{comp_type}' not supported.")

    def compare_test_all(X,Y):
        print(f"\n> {X.__class__.__name__}")
        print('-'*60)

        for comp in comps:
            compare_test_single(X,Y,comp)

    class Compare:
        def __init__(self,value):
            self.data = value
        def __repr__(self):
            return str(self.data)
    
    class CompareLtGt(Compare):
        def __gt__(self,other):
            return self.data > other
        def __lt__(self,other):
            return self.data < other
    
    class CompareLeGe(Compare):
        def __ge__(self,other):
            return self.data >= other
        def __le__(self,other):
            return self.data <= other

    class CompareEqNe(Compare):
        def __eq__(self,other):
            return str(self.data == other) + ' (redefined)'
        def __ne__(self,other):
            return str(self.data != other) + ' (redefined)'
        
    class CompareAll(CompareLtGt,CompareLeGe,CompareEqNe):
        pass

    comp_with = 'ham'
    L = []
    L.append(Compare('spam'))
    L.append(CompareLtGt('spam'))
    L.append(CompareLeGe('spam'))
    L.append(CompareEqNe('spam'))
    L.append(CompareAll('spam'))

    for x in L:
        compare_test_all(x,comp_with)

def bool_tests():
    print("\nBOOLEAN TESTS")

    print("> every object is inherently true or false")
    print("> for classes we can define what this means for objects")

    print("> with __bool__ (preferred for truth tests)")
    
    class Truth:
        def __bool__(self):
            return True

    class NotTruth:
        def __bool__(self):
            return False    

    X = Truth()
    Y = NotTruth()

    print(f"> is X 'True' ? {bool(X)} (always returns True)")
    print(f"> is Y 'True' ? {bool(Y)} (always returns False)")

    print("> with __len__ (if no __bool__, measures length, nonzero=True)")
    
    class LenTruth:
        def __len__(self):
            return 1
    
    class LenNotTruth:
        def __len__(self):
            return 0

    X = LenTruth()
    Y = LenNotTruth()

    print(f"> is X 'True' ? {bool(X)} (always returns True)")
    print(f"> is Y 'True' ? {bool(Y)} (always returns False)")

    print("> with both methods present, bool is preferred")

    class SubTruth(Truth,LenNotTruth):
        pass

    class SubNotTruth(NotTruth,LenTruth):
        pass

    X = SubTruth()
    Y = SubNotTruth()

    print(f"> is X 'True' ? {True if X else False} (always returns True)")
    print(f"> is Y 'True' ? {True if Y else False} (always returns False)")

    class TestTruth:
        pass

    Z = TestTruth()

    print(f"> if no bool or len, object is 'True' by default")
    print(f"> is Z 'True' ? {True if Z else False} (always returns True)")

def object_del():
    print("\nOBJECT DESTRUCTION")

    print("> destruction method __del__ is run when inst. space is being reclaimed")

    class Life:
        def __init__(self,name='unknown'):
            print(f"Hello {name}.")
            self.name = name
        def live(self):
            print(f"> {self.name} is alive.")
        def __del__(self):
            print(f"Goodbye {self.name}.")
    
    X = Life('Brian')
    X.live()
    X = Life('Loretta') # reassign happens before destruction!
    X.live()
    del X

    # not commonly used:
    # > need: not very useful because of gc and autoclose
    # > predictability: hard to predict when an inst. will be reclaimed
    # > exceptions: raised exc print a warning instead of triggering events
    # > cycles: circular references may prevent gc from happening
