from typing import Any

def extend_built_ins_embed():
    print("\nEXTENDING BUILT-IN TYPES: EMBEDDING")
    
    print("\n> new set object type with methods and o.o, wraps list")

    class Set:
        def __init__(self,value=[]):
            self.data = []
            self.concat(value)
        
        def concat(self,value):
            for x in value:                 # value: list, Set, ...
                if not x in self.data:      # removes duplicates
                    self.data.append(x)
        
        def intersect(self,other):          # other is any sequence
            result = []                     # self is the subject
            for x in self.data:
                if x in other:              # pick common items
                    result.append(x)
            return Set(result)              # return a new Set
    
        def union(self,other):              # other is any sequence
            result = self.data[:]           # copy of my list
            for x in other:                 # add items in order
                if not x in result:
                    result.append(x)
            return Set(result)              # return a new Set
    
        def __len__(self):          return len(self.data)           # len(self), if self
        def __getitem__(self,key):  return self.data[key]           # self[i], self[i:j]
        def __and__(self,other):    return self.intersect(other)    # self & other
        def __or__(self,other):     return self.union(other)        # self | other
        def __repr__(self):         return f"Set: {repr(self.data)}"# print(self),...
        def __iter__(self):         return iter(self.data)          # for x in self,...
    
    X = Set([1,3,5,7])
    print(f"> set X initialized to: {X}")
    print(f"> > len(X) = {len(X)}")
    print(f"> > X[0] = {X[0]}")

    Y = Set([1,4,7])
    print(f"> set Y initialized to: {Y}")
    print(f"> > len(Y) = {len(Y)}")
    print(f"> > Y[0] = {Y[0]}")

    U = X.union(Y)
    print(f"> set U union X | Y: {U}")
    print("> > list elements: ",end='')
    for u in U: print(u,end=' | ')
    print()

    I = X.intersect(Y)
    print(f"> set I intersect X & Y: {I}")
    print("> > list elements: ",end='')
    for i in I: print(i,end=' | ')
    print()

def extend_built_ins_subclass():
    print("\nEXTENDING BUILT-IN TYPES: SUBCLASSING")

    print("\n> subclass list, map 1..N to 0..N-1; call back to built-in")

    class MyList(list):
        def __getitem__(self,offset):
            print(f"(indexing {self} at {offset})")
            return list.__getitem__(self,offset-1)
    
    S = 'abc'; Lb = list(S); Lm = MyList(S)     # init inherited from list
    
    print("\nINIT:")
    print(f"> built-in list: {Lb}")
    print(f"> custom list: {Lm}")

    print("\nGETITEM:")
    print(f"> built-in list [1]: {Lb[1]}")
    print(f"> custom MyList [1]: {Lm[1]}")

    a = 'spam'; Lb.append(a); Lm.append(a)      # attrs from list super

    print(f"\nAPPEND '{a}':")
    print(f"> built-in list: {Lb}")
    print(f"> custom MyList: {Lm}")

    Lb.reverse(); Lm.reverse()

    print("\nREVERSE:")
    print(f"> built-in list: {Lb}")
    print(f"> custom MyList: {Lm}")

    print("\n> customized list with added methods and ops related to sets")

    class Set(list):
        def __init__(self,value=[]):
            list.__init__(self)
            self.concat(value)

        def concat(self,value):                 # value: list, Set, ...
            for x in value:                     # removes duplicates
                if not x in self:
                    self.append(x)
        
        def intersect(self,other):              # other is any sequence
            result = []                         # self is the subject
            for x in self:
                if x in other:                  # pick common items
                    result.append(x)
            return Set(result)                  # return a new set
    
        def union(self,other):                  # other is any sequence
            result = Set(self)                  # copy me and my list
            result.concat(other)
            return result
        
        def __and__(self,other):    return self.intersect(other)
        def __or__(self,other):     return self.union(other)
        def __repr__(self):         return f"Set: {list.__repr__(self)}"

    X = Set([1,3,5,7])
    print(f"> set X initialized to: {X}")
    print(f"> > len(X) = {len(X)}")
    print(f"> > X[0] = {X[0]}")

    Y = Set([1,4,7])
    print(f"> set Y initialized to: {Y}")
    print(f"> > len(Y) = {len(Y)}")
    print(f"> > Y[0] = {Y[0]}")

    U = X.union(Y)
    print(f"> set U union X | Y: {U}")
    print("> > list elements: ",end='')
    for u in U: print(u,end=' | ')
    print()

    I = X.intersect(Y)
    print(f"> set I intersect X & Y: {I}")
    print("> > list elements: ",end='')
    for i in I: print(i,end=' | ')
    print()

def stringify(I):
    str_I = str(I).split('.')
    return str_I[0] + (('...'+str_I[-1]) if len(str_I)>1 else '')

def new_style_classes():
    print("\nTHE NEW-STYLE CLASS MODEL")

    def attr_intercept():
        print("\nATTRIBUTE INTERCEPTION")
        print("> in 2.X indexing and prints are routed to __getattr__")
        print("> in 3.X o.o. is neccessary for their customization")

        class C:
            data = 'spam'

            def __getattr__(self,name):         # in 2.X catches built-ins
                print(f"__getattr__: {name}")
                return getattr(self.data,name)
        
        X = C()
        print(f"\n> Class C, data = {X.data}")
        print("> attempt to route indexing through getattr")
        print("> > X[0] = ",end='')
        try:
            print(X[0])
        except Exception as e:
            print(f"error! {e}")

        print("> attempt to route printing through getattr")
        print(f"> > X = {X}")

        print("> does not apply to normally named methods")
        X.normal = lambda: 99
        print(f"> > 'normal' lambda method, returns 99: {X.normal()}")

        print("> does not apply to explicit calls to built-ins by name")
        X.__add__ = lambda y: 88 + y
        print(f"> > __add__ o.o, called by name (88+1): {X.__add__(1)}")

        print(f"> > index using __getitem__(1): {X.__getitem__(1)}")

        print("> applies only to calling built-in operations")
        print(f"> > __add__ called by + (88+1): ",end='')

        try:
            print(X+1)
        except Exception as e:
            print(f"error! {e}")
        
        print("> through-type calling does not get routed")
        print("> > index using type(X).__getitem__(1): ",end='')
        try:
            print(type(X).__getitem__(X,1))
        except Exception as e:
            print(f"error! {e}")

        print("> > __add__ using type(X).__add__(1): ",end='')
        try:
            print(type(X).__add__(X,1))
        except Exception as e:
            print(f"error! {e}")

        class CSub1(C):
            def __getattr__(self,name):
                print(f"__getattr__: {name}")
        
        X = CSub1()
        print("\n> subclassed, getattr set only to print names for testing")
        print(f"> calls to undef.attrs route to getattr (try 'new' attr):",end='')
        X.new
        print(f"> calls to o.o methods route to getattr (try __add__):",end='')
        X.__add__

        print("> getattr for normal names and o.o method redefinitions")
        print("> required for all names accessed by built-in operations!")

        class CSub2(C):
            def __getitem__(self,i):
                print(f'getitem: {str(i)}')
                return self.data[i]
            
            def __add__(self,other):
                print(f"add: {other}")
                return getattr(self.data,'__add__')(other)
        
        X = CSub2()
        X_upper = X.upper
        print("\n> method search (routed through getattr)")
        print(f"> > test search for 'upper' method:\n{X_upper}")
        print(f"> > execute upper method (from str): {X.upper()}")

        print("\n> indexing (routed through o.o)")
        print(f"> built-in operation X[1]: {X[1]}")
        print(f"> explicit call: {X.__getitem__(1)}")
        print(f"> through-type call: {type(X).__getitem__(X,1)}")

        print("\n> adding (routed through o.o)")
        print(f"> built-in operation X+'eggs': {X+'eggs'}")
        print(f"> explicit call: {X.__add__('eggs')}")
        print(f"> through-type call: {type(X).__add__(X,'eggs')}")

    def type_class_merge():
        print("\nCLASSES AND TYPES MERGED")

        print("\n> classes are types, types are classes")

        class C: pass

        I = C()
        print(f"\n> custom class instance: {stringify(I)}")
        print(f"> > type of instance: {stringify(type(I))}")
        print(f"> > instance class: {stringify(I.__class__)}")

        print(f"\n> custom class: {stringify(C)}")
        print(f"> > type of class: {type(C)}")
        print(f"> > class class: {C.__class__}")

        L = [1,2,3]
        print(f"\n> list instance: {L}")
        print(f"> > type of instance: {type(L)}")
        print(f"> > instance class: {L.__class__}")

        print(f"\n> built-in class: {list}")
        print(f"> > type of class: {type(list)}")
        print(f"> > class class: {list.__class__}")

        print("\n> comparing custom classes")      

        class D: pass

        J = D()
        print(f"\n> custom class instance: {stringify(J)}")
        print(f"> > type of instance: {stringify(type(J))}")
        print(f"> > instance class: {stringify(J.__class__)}")

        print(f"\n> custom class: {stringify(D)}")
        print(f"> > type of class: {type(D)}")
        print(f"> > class class: {D.__class__}")

        print(f"\n> every instance is type of its class")
        print(f"> > inst. I&J equal by type? {type(I)==type(J)}")

        print(f"\n> every class is of the same type, 'type'")
        print(f"> > class C&D equal by type? {type(C)==type(D)}")

        print("\n> all classes derive from 'object'")

        S = ''        
        print(f"> > is instance of 'str' an 'object'? {isinstance(S,object)}")
        print(f"> > is class 'str' itself an 'object'? {isinstance(str,object)}")
    	
        print(f"\n> 'type' also derives from 'object'")
        print(f"> > type of 'type' ? {type(type)}")
        print(f"> > is 'type' instance of 'object'? {isinstance(type,object)}")

        print(f"\n> and 'object' derives from 'type'")
        print(f"> > type of 'object' {type(object)}")
        print(f"> > is 'object' instance of 'type'? {isinstance(object,type)}")

        print(f"\n> but 'type' and 'object' are not the same")
        print(f"> > type is object ? {type is object}")
    
    def object_root():
        print("\nAUTOMATIC OBJECT ROOT CLASS")

        print(f"\n> 'object' is root of every class, with its defaults")

        class C: pass
        class D: pass

        print(f"> > class C supers: {C.__bases__}")
        print(f"> > class D supers: {D.__bases__}")

        print(f"> > built-in list supers: {list.__bases__}")
        print(f"> > built-in str supers: {str.__bases__}")

        print(f"> > 'object' defaults:\n{dir(object)}")

    def MRO_diamonds():
        print("\nDIAMOND INHERITANCE CHANGE")

        # classic (2.X) classes: DFLR (depth-first-left-to-right)
        # new-style (3.X) classes: MRO (method-resolution-order)
        # > MRO is more like breadth-first (DF + last occurence lives)

        class A:        attr = 'A'      #    A
        class B(A):     pass            #   / \
        class C(A):     attr = 'C'      #  B   C 
        class D(B,C):   pass            #   \ /
        X = D()                         #    D

        # DFLR: X > D > B > A > finds attr, stops searching; attr = 'A'
        # MRO:  X > D > B > A > finds attr > C > overwrites; attr = 'C'

        print(f"> diamond inheritance, attr = {X.attr}")

        class E(B,C):   attr = A.attr
        X = E()

        print(f"> > inherit from super explicitly, attr = {X.attr}")

        class A:
            def method(self): print('A.method')
        class B(A):
            pass
        class C(A):
            def method(self): print('C.method')
        class D(B,C):
            pass
        X = D()

        print("> diamond inheritance, method = ",end=''); X.method()

        class E(B,C):
            method = A.method
        X = E()

        print(f"> > inherit from super explicitly, method = ",end=''); X.method()

        class F(B,C):
            def method(self): A.method(self)
        X = F()

        print(f"> > inherit from super by call, method = ",end=''); X.method()

        print(f"\n> MRO is a tuple giving the linear search order")

        X = D()
        print(f"\n> > MRO of instance X of class D:")

        print("> > > diamond:")
        class A:        attr = 'A'      #    A
        class B(A):     pass            #   / \
        class C(A):     attr = 'C'      #  B   C 
        class D(B,C):   pass            #   \ /
        X = D()                         #    D
        for x in D.__mro__: print(stringify(x))

        print("> > > 'non' - diamond:")
        class A:        attr = 'A'      #    A
        class B(A):     pass            #   /
        class C:        attr = 'C'      #  B   C 
        class D(B,C):   pass            #   \ /
        X = D()                         #    D
        for x in D.__mro__: print(stringify(x))

        print("> > > 'non' - diamond:")
        class A:        attr = 'A'      #    A
        class B:        pass            #     \
        class C(A):     attr = 'C'      #  B   C 
        class D(B,C):   pass            #   \ /
        X = D()                         #    D
        for x in D.__mro__: print(stringify(x))

        print("> > > diamond through object")
        class X: pass                   # X   Y
        class Y: pass                   # |   |
        class A(X): pass                # A   B
        class B(Y): pass                #  \ /
        class D(A,B): pass              #   D
        I = D()
        for x in D.__mro__: print(stringify(x))

        print("\n> > collect only class names from MRO:")
        print([cls.__name__ for cls in D.__mro__])
    
    def map_attrs_to_source():
        print("\nEXAMPLE: MAPPING ATTRIBUTES TO INHERITANCE SOURCES")

        import mapattrs as ma

        import numpy as np
        I = np.ndarray((2,2))
        ma.trace(ma.mapattrs(I,bysource=True))

    def slots_basics():
        print("\nSLOTS BASICS")

        class limiter:
            __slots__ = ['age','name','job']
        
        X = limiter()

        print("> X init to 'limited' class")
        print(f"> > available slots: {limiter.__slots__}")
        X.age = 40
        print(f"> > > assign 40 to 'age': {X.age}")
        print(f"> > > assign 40 to 'ape': ",end='')
        try:
            print(X.ape)
        except Exception as e:
            print(f"error!\n{e}")
        print("> > if slots, no dict initialized")
        print("> > > __dict__ content: ",end='')
        try:
            print(X.__dict__)
        except Exception as e:
            print(f"error!\n{e}")
        print("> > still can fetch with getattr")
        print(f"> > > get 'age': {getattr(X,'age')}")
        print("> > still can set with setattr")
        setattr(X,'name','Bob')
        print(f"> > > set 'name' to 'Bob': {X.name}")
        print("> > dir() finds slot attributes")
        print(f"> > > 'age' in dir ? {'age' in dir(X)}")
        print(f"> > > 'ape' in dir ? {'ape' in dir(X)}")
        print(f"> > > 'name' in dir ? {'name' in dir(X)}")

        class C:
            __slots__ = ['a','b']
            def __init__(self):
                self.c = 3
        
        print("> > without dict cannot assign new names apart from slots")
        print("> > > try to init inst. X of C and set new name: ",end='')
        try:
            X = C()
            print("OK!")
        except Exception as e:
            print(f"error!\n{e}")
        
        class D:
            __slots__ = ['a','b','__dict__']
            def __init__(self):
                self.c = 3
        
        print("> > if we add dict to slots, can assign new names")
        print("> > > try to init inst. X of D and set new name: ",end='')
        X = D()
        try:
            X = C()
            print("OK!")
        except Exception as e:
            print(f"error!\n{e}")
        
        X.a = 1
        X.b = 2

        print(f"> > X slots: {X.__slots__}")
        print(f"> > X dict: {X.__dict__}")

        print("> > getattr fetches both dict and slots:")
        print(f"> > > a = {getattr(X,'a')}")
        print(f"> > > b = {getattr(X,'b')}")
        print(f"> > > c = {getattr(X,'c')}")

        class E(D):
            __slots__ = ['c','d']
        
        X = E()
        X.a = 1; X.b = 2; X.c = 3; X.d = 4; X.e = 5

        print("> slots become class-level attributes")
        print("> inst. acquires union of all slot names")
        print("> but they are not concatenated")
        print(f"> > D slots: {D.__slots__}")
        print(f"> > E slots: {E.__slots__}")
        print(f"> > X slots: {X.__slots__}")
        print(f"> > X dict: {X.__dict__} < because of D dict in slots")
        print(f"> X names: .a={X.a} .b={X.b} .c={X.c} .d={X.d} .e={X.e}")
        print("> search through dict and slots will miss super")
        print("> > but dir() will include all: (filter private)")
        print([x for x in dir(X) if not x.startswith('__')])

        class F(D):
            def __init__(self,data):
                self.c = data
        
        X = F(3)

        print("> if dict in slots, can init with arg data as usual")
        print(f"> > X.c = {X.c}")

        print("> slots in subs are pointless when absent in supers")
        # > because __dict__ from super will always be available
        class C: pass
        class D(C): __slots__ = ['a']
        X = D(); X.a = 1; X.b = 2
        print(f"> > X: .a={X.a} < from slots sub .b={X.b} < from super")

        print("> slots in supers are pointless when absent in subs")
        # > because __dict__ from sub will always be available
        class C: __slots__ = ['a']
        class D(C): pass
        X = D(); X.a = 1; X.b = 2
        print(f"> > X: .a={X.a} < from slots super .b={X.b} < from sub")

        print("> redefinition renders super slots pointless")
        # > if sub redefines super's slot name, only sub's is accessible
        class C: __slots__ = ['a']
        class D(C): __slots__ = ['a']
        X = D(); X.a = 1
        print(f"> > X: .a={X.a} < from sub (redefined)")

        print("> slots prevent class-level defaults")
        # > cannot use class attrs of same name to provide defaults (override)
        print("> > try to create class with slot 'a' with def. value in class")
        try:
            class C: __slots__ = ['a']; a = 99
        except Exception as e:
            print(f"> > error! {e}")
        # X = C(); X.a = 1  
        
        print("> slots and __dict__: slots preclude dict")
        # > if dict in slots, they are pointless (all names available)
        print("> > we cannot assume class has a dict (if slots no dict init)")
        print("> > before searching through inst. dict, check if it's there")
        
        class C: __slots__ = ['a']
        X = C()

        print("> > > search for 'attr' in dict: ")

        print("> > > (with default): ",end='')
        if 'attr' in getattr(X,'__dict__',{}):
            print("dict present, 'attr' in dict")
        else:
            print("dict not present or attr not in dict")

        print("> > > (explicit check): ",end='')
        if hasattr(X,'__dict__') and 'attr' in X.__dict__:
            print("dict present, 'attr' in dict")
        else:
            print("dict not present or attr not in dict")

    def properties_basics():
        print("\nPROPERTIES BASICS")

        print("\n> getattr allows classes to intercept undefined attr refs")

        class operators_g:
            def __getattr__(self,name):
                if name == 'age':
                    return 40
                else:
                    raise AttributeError(name)
        
        X = operators_g()
        print("> X init to operators")
        print("> > try to fetch undefined attributes")
        print(f"> > > 'age' : {X.age}")
        print(f"> > > 'other' : ",end='')
        try:
            print(X.other)
        except Exception as e:
            print(f"error! attribute error: {e}")
        
        print("\n> same example coded with properties")

        class properties_g:
            def get_age(self):
                return 40
            age = property(get_age,None,None,None)
        
        X = properties_g()
        print("> X init to properties")
        print("> > try to fetch undefined attributes")
        print(f"> > > 'age' : {X.age}")
        print(f"> > > 'other' : ",end='')
        try:
            print(X.other)
        except Exception as e:
            print(f"error! {e}")

        print("\n> with attribute assignment support")

        class properties_gs(properties_g):
            def set_age(self, value):
                print(f"set age: {value}")
                self._age = value
            age = property(properties_g.get_age,set_age,None,None)
        
        X = properties_gs()
        X.age = 42
        print(f"> X._age (internal): {X._age}")
        print(f"> X.age (runs get_age): {X.age}")
        X.job = 'trainer'
        print(f"> X.job (normal): {X.job}")

        print("\na.a. support with operators")

        class operators_gs(operators_g):
            def __setattr__(self, name, value):
                print(f"set {name}: {value}")
                if name == 'age':
                    self.__dict__['_age'] = value
                else:
                    self.__dict__[name] = value
        
        X = operators_gs()
        X.age = 42
        print(f"> X._age (internal): {X._age}")
        print(f"> X.age (runs getattr): {X.age}")
        X.job = 'trainer'
        print(f"> X.job (normal): {X.job}")
                            
    def get_attribute():
        print("\n__GETATTRIBUTE__ AND DESCRIPTORS: ATTRIBUTE TOOLS")

        print("\n> getattribute o.o")
        print("> > intercepts all attr refs (not just undefined ones)")
        print("> > more potent than getattr but trickier to use")

        print("\n> attribute descriptors")
        print("> > classes with get&set, assigned to class attrs")
        print("> > intercept read&write accesses to specific attrs")

        class AgeDescriptor:
            def __get__(self,instance,owner): return 40
            def __set__(self,instance,value): instance._age=value
        
        class descriptors:
            age = AgeDescriptor()
        
        X = descriptors()
        print("> X init to descriptors")
        print(f"> > X age: {X.age}")                # A.S.__get__
        X.age = 42                                  # A.S.__set__
        print(f"> > X age changed to {X._age}")     # normal fetch

    # attr_intercept()
    # type_class_merge()
    # object_root()
    # MRO_diamonds()
    # map_attrs_to_source()
    # slots_basics()
    # properties_basics()
    # get_attribute()

def static_and_class_methods():
    print("\nSTATIC AND CLASS METHODS")

    # instance counters

    print("\n1) class with counter stored as a class attribute")

    class Spam:
        numInstances = 0

        def __init__(self):
            Spam.numInstances += 1

        def printNumInstances():
            print(f"Number of instances created: {Spam.numInstances}")
    
    a = Spam()
    b = Spam()
    c = Spam()

    print("> Call class method through class:")
    Spam.printNumInstances()
    print("> Call class method through inst: ",end='')
    try:
        a.printNumInstances()
        b.printNumInstances()
        c.printNumInstances()
    except Exception as e:
        print(f"error!\n{e}")

    print("\n2) access counter using normal functions outside the class")
    def printNumInstances():
        print(f"Number of instances created: {Spam.numInstances}")
    
    printNumInstances()
    print("> problem is that f can be too far removed")
    print("> and it cannot be changed via inheritance")

    print("\n3) access counter using normal method, always calling through inst")

    class Eggs(Spam):

        def printNumInstances(self):
            print(f"Number of instances created: {Spam.numInstances}")

    a = Eggs()
    b = Eggs()
    c = Eggs()

    print("> Call inst method through instance")
    a.printNumInstances()
    print("> call inst method through class + instance")
    Eggs.printNumInstances(a)
    print("> call inst method through executing class")
    Eggs().printNumInstances()
    print("> unworkable if we don't have an inst available")
    print("> making an instance changes the class data")

    print("\n*) static and class methods (don't require inst arg)")

    class Methods:
        def i_method(self,x):
            print([self,x])
        
        def s_method(x):
            print([x])
        s_method = staticmethod(s_method)
        
        def c_method(cls,x):
            print([cls,x])
        c_method = classmethod(c_method)

    obj = Methods()
    value = 'some_value'
    print("> > normal instance methods (default)")
    obj.i_method(value)
    print("> > static methods (no instance passed)")
    print("> > > call through instance")
    obj.s_method(value)
    print("> > > call through class")
    Methods.s_method(value)
    print("> > class methods (gets class, not instance)")
    Methods.c_method(value)

    print("\n4) access counter using static methods")

    class Toast(Spam):
        printNumInstances = staticmethod(Spam.printNumInstances)
    
    a = Toast()
    b = Toast()
    c = Toast()

    print("> call static method through class")
    Toast.printNumInstances()
    print("> call static method through instance")
    a.printNumInstances()

    class Ham(Toast):
        def printNumInstances():
            print("do some stuff ...")
            Toast.printNumInstances()
            print("do other stuff ...")
        
        printNumInstances = staticmethod(printNumInstances)
    
    a = Ham()
    b = Ham()
    c = Ham()

    print("\n*) subclass, add functionality")

    print("> call static method through class")
    Ham.printNumInstances()
    print("> call static method through instance")
    a.printNumInstances()

    print("\n5) access counter using class methods")

    class Fruit(Spam):

        def printNumInstances(cls):
            print(f"Number of instances created: {cls.numInstances}")
            print(f"Class: {cls}")
        printNumInstances = classmethod(printNumInstances)

    a = Fruit()
    b = Fruit()
    c = Fruit()

    print("> call static method through class")
    Fruit.printNumInstances()
    print("> call static method through instance")
    a.printNumInstances()

    print("\n*) lowest class passed in even for subs without class methods")

    class Other(Fruit): pass

    a = Other()
    b = Other()
    c = Other()

    print("> call static method through class")
    Other.printNumInstances()
    print("> call static method through instance")
    a.printNumInstances()

    print("\n6) passing class methods to inst methods")

    class Salami:

        numInstances = 0

        def count(cls):                 # per-class instance counters
            cls.numInstances += 1       # cls is lowest class above inst
        count = classmethod(count)

        def __init__(self):             # passes self.__class__ to count
            self.count()
        
    class Bread(Salami):

        numInstances = 0

        def __init__(self):             # redefines __init__
            Salami.__init__(self)
    
    class Butter(Salami):               # inherits __init__

        numInstances = 0
    
    x = Salami()

    y1 = Bread()
    y2 = Bread()

    z1 = Butter()
    z2 = Butter()
    z3 = Butter()
    
    print("> per class data!")
    print("> > using instances")
    print("> > > number of instance of class of instance")
    print(f"x = {x.numInstances} ",end='')
    print(f"y = {y1.numInstances} ",end='')
    print(f"z = {z1.numInstances}")
    print("> > using classes")
    print("> > > number of inst. of class")
    print(f"Salami = {Salami.numInstances} ", end = '')
    print(f"Bread = {Bread.numInstances} ", end='')
    print(f"Butter = {Butter.numInstances}")

def decorators():
    print("\nDECORATORS")

    print("\nFUNCTION DECORATORS")
    print("> augment function definitions - wrapping in extra layer of logic")
    print("> implemented as another function, usually called a metafunction")

    # default syntax:
    class C:
        def method():
            ...
        method = staticmethod(method)   # name rebinding equivalent
    
    # decorator syntax:
    class C:
        @staticmethod                   # function decoration
        def method():
            ...
    
    print("\n> counter example, with function decorator syntax")

    class Counter:

        numInstances = 0

        def __init__(self):
            Counter.numInstances += 1
        
        @staticmethod
        def printNumInstances():
            print(f"Number of instances created: {Counter.numInstances}")

    a = Counter()
    b = Counter()
    c = Counter()

    print("> call static method through class:")
    Counter.printNumInstances()
    print("> call static method through instance:")
    a.printNumInstances()

    print("\n> static + class + property")

    class Methods:

        def i_method(self, value):
            print([self, value])
        
        @staticmethod                   # static: no instance passed
        def s_method(value):
            print([value])
        
        @classmethod                    # class: gets class, not instance
        def c_method(cls, value):
            print([cls, value])
        
        @property
        def name(self):
            return 'Bob ' + self.__class__.__name__
    
    obj = Methods()
    value = 'some value'
    print("> > instance method: ",end=''); obj.i_method(value)
    print("> > static method: ",end=''); obj.s_method(value)
    print("> > class method: ",end=''); obj.c_method(value)
    print(f"> > 'name' property: {obj.name}")
        
    print("\n> user-defined function decorators")

    class Tracer:

        def __init__(self,func):
            self.calls = 0
            self.func = func
        
        def __call__(self,*args):
            self.calls += 1
            print(f"Call {self.calls} to {self.func.__name__}")
            return self.func(*args)
    
    @Tracer                         # wrap function in a decorator object
    def add_three(a,b,c):           # same as f = Tracer(f)
        return a + b + c
    
    print("> add three (1,2,3):")
    print(add_three(1,2,3))         # really calls the tracer wrapper object
    print("> add three (a,b,c):")
    print(add_three('a','b','c'))   # really calls the tracer wrapper object

    print("\n> closure based equivalent")

    def tracer_func(func):
        def oncall(*args):
            oncall.calls += 1
            print(f"Call {oncall.calls} to {func.__name__}")
            return func(*args)
        oncall.calls = 0
        return oncall
    
    class C:
        @tracer_func
        def add_three(self,a,b,c):
            return a + b + c
        
    x = C()
    
    print("> add three (1,2,3):")
    print(x.add_three(1,2,3))
    print("> add three (a,b,c):")
    print(x.add_three('a','b','c'))

    print("\n> user-defined class decorators")

    # default syntax:
    def decorator(klass):
        ...
    
    class C:
        ...
    C = decorator(C)

    # decorator syntax
    def decorator(klass):
        ...
    
    @decorator
    class C:
        ...
    
    print("> counter example, with class decorator syntax")

    def count(klass):
        klass.numInstances = 0
        return klass
    
    @count
    class Spam:

        def __init__(self):
            Spam.numInstances += 1
    
    # a = Spam()
    # b = Spam()
    # c = Spam()

    print("> Attribute initialized through decoration: ",end='')
    print(Spam.numInstances)

    print("> class dec. can manage an entire interface by intercepting")
    print("> construction calls and wrapping the new inst. in a proxy")
    print("> that deploys attr accessor to intercept later requests")

    print("\n> decorator with proxy (preview)")

    def decorator(cls):
        class Proxy:

            def __init__(self,*args):
                self.wrapped = cls(*args)

            def __getattr__(self,name):
                print("[Routing through proxy object] ... ",end='')
                return getattr(self.wrapped,name) if hasattr(self.wrapped,name) else f"no attr '{name}'"
        
        return Proxy

    @decorator
    class D:
        def __init__(self,data):
            self.data = data

    X = D('spam')
    print("> class D initialized, data attr value:")
    print(X.data)
    print("> fetch unknown attr 'name' value:")
    print(X.name)


    print("\n> metaclass equivalent (preview)")
    class MetaNew(type):
        def __new__(meta,classname,supers,classdict):
            print("[class creation routed through metaclass]")
            print("...extra logic + class creation via type call...")

            print(f"> meta: {meta}")
            print(f"> classname: {classname}")
            print(f"> supers: {supers}")
            print(f"> classdict: {classdict}")

            x = super().__new__(meta,classname,supers,classdict)
            x.attr = 100

            print(f"> attr default: {x.attr}")

            return x
    
    class Mixin: ...

    class M1(metaclass=MetaNew): ...          # like M1 = Meta('M1',(),{...})
    class M2(Mixin,metaclass=MetaNew):  ...   # like M2 = Meta('M2',(Mixin),{...})

    print("\n> classes M1, M2 initialized (metaclass = MetaNew")
    print("> 'attr' default from meta:")
    print(f"> > M1.attr = {M1.attr}")
    print(f"> > M2.attr = {M2.attr}")

    class MetaInit(type):
        def __init__(meta,classname,supers,classdict):

            print(f"> meta: {meta}")
            print(f"> classname: {classname}")
            print(f"> supers: {supers}")
            print(f"> classdict: {classdict}")

            meta.attr = 100
    
    class X(metaclass=MetaInit): ...
    class Y(metaclass=MetaInit): ...
    class Z(metaclass=MetaInit): ...

    print("\n> classes X,Y,Z initialized (metaclass = MetaInit)")
    print("> 'attr' default from meta:")
    print(f"> > X.attr = {X.attr}")
    print(f"> > Y.attr = {Y.attr}")
    print(f"> > Z.attr = {Z.attr}")

def super_built_in():
    print("\nTHE SUPER BUILT-IN FUNCTION")

    def super_built_in_basic():

        print("\n> traditional form: name superclass explicitly, pass self")

        class C:
            def act(self):
                print('in class C (super)')
                print(self)
        
        class D(C):
            def act(self):
                C.act(self)
                print("in class D (sub)")
                print(self)
        
        X = D()
        X.act()

        print("\n> using super to name superclass generically, omit self")

        class E(C):

            def act(self):
                super().act()
                print("in class E (sub)")
                print(self)

            def method(self):
                proxy = super()
                print("> show the normally hidden proxy object")
                print(proxy)
                print("> implicitly call superclass method (no args)")
                proxy.act()
        
        Y = E()
        Y.act()
        Y.method()

    def multiple_inheritance():
        
        print("\n> adding multiple inheritance naively")

        class A:
            def act(self):
                print("in class A (super)")
                print(self)
        
        class B:
            def act(self):
                print("in class B (super)")
                print(self)
        
        class C(A,B):
            def act(self):
                super().act()
                print("in class C (sub)")
                print(self)
        
        X = C()
        print("> > super silently picks up the leftmost class")
        X.act()

        class D(A,B):
            def act(self):
                A.act(self)
                B.act(self)

        Y = D()
        print("> > calling supers explicitly avoids confusion")
        Y.act()

    def operator_overloading():

        print("\n> limitation: operator overloading")

        class C:
            def __init__(self,value):
                self.data = value

            def __getitem__(self,ix):
                print(f"[class C index: {ix}] ",end='')
                if ix>=0 and ix < len(self.data)-1:
                    return self.data[ix]
                else:
                    print("error! ",end='')
                    return None

        class D(C):
            def __getitem__(self,ix):
                print(f"[class D index: {ix}] ",end='')
                return C.__getitem__(self,ix)
        
        class E(C):
            def __getitem__(self,ix):
                print(f"[class E index: {ix}] ",end='')
                return super().__getitem__(ix)
        
        class F(C):
            def __getitem__(self,ix):
                print(f"[class F index: {ix}] ",end='')
                try:
                    return super()[ix]
                except Exception as e:
                    print("error! ",end='')
                    return e

        value = [1,2,3,4]

        print(f"value = {value}")
        X = C(value)
        print("\nX >> class C")
        print(f"X[0] = {X[0]}")
        print(f"X[4] = {X[4]}")
        Y = D(value)
        print("\nY >> class D")
        print(f"Y[1] = {Y[1]}")
        print(f"Y[5] = {Y[5]}")
        Z = E(value)
        print("\nZ >> class E")
        print(f"Z[2] = {Z[2]}")
        print(f"Z[6] = {Z[6]}")
        W = F(value)
        print("\nW >> class F")
        print(f"W[3] = {W[3]}")
        print(f"W[7] = {W[7]}")

    def dynamic_tree_changes():

        print("\n> useful when a superclass may be changed at runtime")
        # > it is not possible to hardcode its name in a call expression

        class A:
            def method(self):
                print("in class A")

        class B:
            def method(self):
                print("in class B")

        class C(A):
            def method(self):
                print("in class C")
                super().method()

        print("> init instance")
        X = C()
        print("> call method")
        X.method()
        print("> change bases")
        C.__bases__ = (B,)
        print("> call method")
        X.method()

        class D(A):
            def method(self):
                print("in class D")
                D.__bases__[0].method(self)

        print("\n> alternative: use [super].__bases__[#] in sub")

        print("> init instance")
        X = D()
        print("> call method")
        X.method()
        print("> change bases")
        D.__bases__ = (B,)
        print("> call method")
        X.method()

    def cooperative_dispatch():

        print("\nCOOPERATIVE DISPATCH")
        print("> useful when multiple inheritance trees must")
        print("> dispatch to same-name methods in multiple classes")
        # > can be used as a protocol for orderly call routing

        def note_1_disjoint_branches():
        
            print("\n1) sub with disjoint tree branches, trad. coding")

            class A:
                def __init__(self):
                    print("in class A")
            
            class B:
                def __init__(self):
                    print("in class B")
            
            class C(A,B): pass

            print("> runs leftmost super only by default")
            X = C()

            class D(A,B):
                def __init__(self):
                    B.__init__(self)
                    C.__init__(self)
            
            print("> invoke supers explicitly by name")
            Y = D()

        def note_2_multiple_triggers():
        
            print("\n2) diamond pattern may trigger top-level more than once")

            class A:
                def __init__(self):
                    print("in class A")
                
            class B(A):
                def __init__(self):
                    print("in class B")
                    A.__init__(self)
            
            class C(A):
                def __init__(self):
                    print("in class C")
                    A.__init__(self)
            
            print("> B sub of A runs itself then A")
            X = B()

            print("> C sub of A runs itself then A")
            Y = C()
            
            class D(B,C): pass

            print("> D sub of B,C implicitly runs B>A")
            print("> still runs leftmost by default")
            Z = D()

            class E(B,C):
                def __init__(self):
                    B.__init__(self)
                    C.__init__(self)
        
            print("> invoke supers explicitly by name")
            print("> E sub of B,C runs B>A then C>A")
            W = E()
    
        def note_3_MRO_dispatch():
        
            print("\n3) if all use super, calls are dispatched following MRO")

            class A:
                def __init__(self):
                    print("in class A")

            class B(A):
                def __init__(self):
                    print("in class B")
                    super().__init__()
            
            class C(A):
                def __init__(self):
                    print("in class C")
                    super().__init__()
            
            print("> B sub of A runs itself then A")
            X = B()

            print("> C sub of A runs itself then A")
            Y = C()

            class D(B,C): pass

            print("> D sub of B,C with super runs B>C>A per MRO")
            Z = D()
            print("> D MRO:")
            [print(stringify(x)) for x in D.__mro__]

        def note_4_constraint():
        
            print("\n4) constraint: call chain anchor requirement")

            print("> all sub from object > MRO can be used if diamond implicit")
            print("> object is an implied super at the end of MRO")

            class A:
                def __init__(self):
                    print("in class A")
                    super().__init__()
            
            class B:
                def __init__(self):
                    print("in class B")
                    super().__init__()
            
            class C(A,B): pass
            
            print("> C sub of A,B runs A then B per MRO")
            X = C()
            print(f"C MRO: {[stringify(x) for x in C.__mro__]}")

            print("> this is 'lucky' > object has __init__, it ends the chain")
            print("> in most cases it won't have suitable default method")
            print("> most trees require explicit (extra) super as anchor")

        def note_5_scope():
        
            print("\n5) scope: all-or-nothing model")

            print("> if any class fails to pass along the call chain")
            print("> it ends the chain prematurely and the structure fails")

            class A:
                def __init__(self):
                    print("in class A")
                    # super().__init__()
            
            class B:
                def __init__(self):
                    print("in class B")
                    super().__init__()
            
            class C(A,B): pass

            print("> C sub of A,B runs A then stops (A misses super call)")
            X = C()

        def note_6_flexibility():
        
            print("\n6) flexibility: call ordering assumptions")
            print("> what if method call ordering needs differ from MRO?")

            class B:
                def __init__(self):
                    print("in class B")
                    super().__init__()
            
            class C:
                def __init__(self):
                    print("in class C")
                    super().__init__()

            class D(B,C):
                def __init__(self):
                    print("in class D")
                    C.__init__(self)
                    B.__init__(self)

            print("> MRO still applies, to circumvent use explicit calls")
            X = D()
    
        def note_7_customization():

            print("\n7) customization: method replacement")
            print("> super() expectations make it difficult to replace methods")

            class A:
                def method(self):
                    print("method in class A")
                    super().method()
            
            class B(A):
                def method(self):
                    print("method in class B")
                    super().method()
            
            class C:
                def method(self):
                    print("method in class C")
                    # no super: must anchor the chain
            
            class D(B,C):
                def method(self):
                    print("method in class D")
                    super().method()
            
            print("> dispatch to all per MRO automatically: B>A>C")
            X = D()
            X.method()
            
            print("> method replacement breaks the super model")

            class B(A):
                def method(self):
                    print("method in class B (replaced)")
                    # super().method()  # dropped in replaced method
            
            class D(B,C):
                def method(self):
                    print("method in class D")
                    super().method()
            
            print("> dispatch to all until stop: B (misses super)")
            X = D()
            X.method()

            class D(B,C):
                def method(self):
                    print("method in class D")
                    B.method(self)
                    C.method(self)
            
            print("> still works with explicit super calls")
            X = D()
            X.method()

        def note_8_coupling():
            print("\n8) coupling: application to mix-in classes")
            print("> classes in MRO without the method searched are skipped")

            class A:
                def other(self):
                    print("other: in class A")
            
            class Mixin(A):
                def other(self):
                    print("other: in class Mixin")
                    super().other()
            
            class B:
                def method(self):
                    print("method: in class B")
            
            class C(Mixin,B):
                def method(self):
                    print("method: in class C")
                    super().other()
                    super().method()
            
            print("\n> super().other() skips B (no 'other' in B)")
            print("> super().method() skips Mixin & A, reaches B")

            X = C()
            X.method()

            print("\n> chains work even if a branch doesn't use super")
            print("> as long as the method is defined somewhere ahead in MRO")

            class C(B,Mixin):
                def method(self):
                    print("method: in class C")
                    super().other()
                    super().method()
            
            print("\n> super().other() skips B, reaches Mixin>A")
            print("> super().method() skips Mixin & A (no 'method' in them)")
            
            X = C()
            X.method()

            print(f"\n> C MRO:")
            [print(stringify(x)) for x in C.__mro__]

            print("\n> this is also true in the presence of diamonds")
            print("> MRO is the same, the case is equivalent to non-diamond")
            
            class B(A):
                def method(self):
                    print("method: in class B")
            
            class C(Mixin,B):
                def method(self):
                    print("method: in class C")
                    super().other()
                    super().method()
            
            print("\n> subclass always appears before its superclass in the MRO")
            print("> super().other() still reaches A from Mixin")

            X = C()
            X.method()

            print("\n> other mix-in call orderings will work too")
            print("> as long as the search finds the method needed")

            class C(B,Mixin):
                def method(self):
                    print("method: in class C")
                    super().other()
                    super().method()

            X = C()
            X.method()

            print(f"\n> C MRO:")
            [print(stringify(x)) for x in C.__mro__]

            print("\n> using explicit calls here is much simpler")

            class C(B,Mixin):
                def method(self):
                    print("method: in class C")
                    Mixin.other(self)
                    B.method(self)
            
            X = C()
            X.method()

            print("\n> if methods are nondisjoint super creates overly strong coupling")

            class A:
                def method(self):
                    print("method: in class A")
            
            class Mixin(A):
                def method(self):
                    print("method: in class Mixin")
                    super().method()
            
            class B(A):
                def method(self):
                    print("method: in class B")
                    # super().method()  # here would invoke A after B
            
            class C(Mixin,B):
                def method(self):
                    print("method: in class C")
                    super().method()
            
            print("\n> the call to method in Mixin runs A's version as expected")
            print("> unless it's mixed into a tree that drops the call chain")

            X = C()
            X.method()

            print("\n> B's method breakes the chain, no super() call")
            print("> so A's method is not called (may be unexpected)")

            print("\n> explicit calls are immune to context of use")

            class A:
                def method(self):
                    print("method: in class A")
            
            class Mixin(A):
                def method(self):
                    print("method: in class A")
                    A.method(self)
            
            class B(A):
                def method(self):
                    print("method: in class B")
            
            class C(Mixin,B):
                def method(self):
                    print("method: in class C")
                    Mixin.method(self)
            
            print("\n> method in class Mixin>A is called explicitly")
            print("> class B in MRO cannot suppress the call")

            X = C()
            X.method()

            print("\n> making mixins more self contained minimizes component coupling")
            print("> fundamental software principle: reducing program complexity")

        def note_9_customization():
        
            print("\n9) customization: same-argument constraints")
            print("> all super versions must accept the same args list")
            print("> or choose its inputs with analysis of generic args list!")
            print("> example: pizza shop, passing salary argument")

            print("\nV1: explicit calls")

            class Employee:
                def __init__(self,name,salary):
                    self.name = name
                    self.salary = salary
            
            class ChefV1(Employee):
                def __init__(self,name):
                    Employee.__init__(self,name,50000)
            
            class ServerV1(Employee):
                def __init__(self,name):
                    Employee.__init__(self,name,40000)
            
            print("> expected salary arg filled in automatically on sub init")
            bob = ChefV1('Bob')
            sue = ServerV1('Sue')
            print(f"> Chef: {bob.name}, salary: {bob.salary}")
            print(f"> Server: {sue.name}, salary: {sue.salary}")

            print("\nV2: using super")

            class ChefV2(Employee):
                def __init__(self,name):
                    super().__init__(name,50000)
            
            class ServerV2(Employee):
                def __init__(self,name):
                    super().__init__(name,40000)
            
            print("> works for sub in isolation (MRO includes only self and super)")
            bob = ChefV2('Bob')
            sue = ServerV2('Sue')
            print(f"> Chef: {bob.name}, salary: {bob.salary}")
            print(f"> Server: {sue.name}, salary: {sue.salary}")

            class TwoJobs0(ChefV2,ServerV2): pass

            print("> breaks when sub is inheriting both supers - different args list!")
            try:
                tom = TwoJobs0('Tom')
            except Exception as e:
                print(f"init error! {e}")
            print("> problem is init doesn't call super, it calls sibling per MRO")

            print("TwoJobs MRO:")
            [print(stringify(x)) for x in TwoJobs0.__mro__]

            class TwoJobsA(ChefV1,ServerV1): pass
            class TwoJobsB(ServerV1,ChefV1): pass            

            print("\n> explicit calls works with mixed classes")
            print("> dubious results, calls the leftmost class")

            tom = TwoJobsA('Tom')
            print(f"> Two jobs: {tom.name}, salary: {tom.salary}")

            tom = TwoJobsB('Tom')
            print(f"> Two jobs: {tom.name}, salary: {tom.salary}")

            print("\n> we want to route the call ti top-level with new salary")

            print("> works with explicit calls:")

            class TwoJobsC(ChefV1,ServerV1):
                def __init__(self,name):
                    Employee.__init__(self,name,70000)

            tom = TwoJobsC('Tom')
            print(f"> Two jobs: {tom.name}, salary: {tom.salary}")

            print("> doesn't work with super():")

            class TwoJobs1(ChefV2,ServerV2):
                def __init__(self,name):
                    super().__init__(name,70000)
            try:
                tom = TwoJobs1('Tom')
            except Exception as e:
                print(f"init error! {e}")

        # note_1_disjoint_branches()
        # note_2_multiple_triggers()
        # note_3_MRO_dispatch()
        # note_4_constraint()
        # note_5_scope()
        # note_6_flexibility()
        # note_7_customization()
        # note_8_coupling()
        # note_9_customization()

    # super_built_in_basic()
    # multiple_inheritance()
    # operator_overloading()
    # dynamic_tree_changes()
    # cooperative_dispatch()

super_built_in()
