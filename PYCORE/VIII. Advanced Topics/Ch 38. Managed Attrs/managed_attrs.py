def motivation():
    print("\nWHY MANAGE ATTRIBUTES?")

    # suppose you've written a program to use a name attr directly
    # then requirementss change - you decide names should be validated
    # it's easy to code methods to manage access to the attr's value

    def valid(name):
        return True if name else False
    
    def transform(name):
        return name.upper()

    class Person:
        def __init__(self,name=''):
            self.name = name        
        
        def getName(self):
            if not valid(self.name):
                raise TypeError('cannot fetch name')
            else:
                return transform(self.name)
        
        def setName(self,value):
            if not valid(value):
                raise TypeError('cannot change name')
            else:
                self.name = transform(value)
                return self.name
    
    person = Person()
    print("> init person with name ''")
    print("> > try to get name: ",end='')
    try:
        print(person.getName())
    except TypeError as E:
        print(f"error! {E}")
    print("> > set name to 'name': ",end='')
    person.setName('name')
    print(person.name)

    person = Person('name')
    print("> init person with name 'name'")
    print("> > get person name: ",end='')
    print(person.getName())
    print("> > try to set person name to '': " ,end='')
    try:
        print(person.setName(''))
    except TypeError as E:
        print(f"error! {E}")
    
    # problem is this requires changing all the places where names are used
    # also, this requires the program to be aware how values are exported
    # called methods > clients are immune to changes (changing the method)
    # simple names > can become problematic with time (switching to methods!)

def properties():
    print("\nPROPERTIES")

    # general syntax:
    # attribute = property(fget,fset,fdel,doc)    
    # fget: for attr fetching
    # fset: for attr assignments
    # fdel: for attr deletions
    # doc: docstring for the attr
    # all default to None if args are not passed
    # > means the operation is not supported
    # returns a property object which we assign to
    # the name of thee attr to be managed in class scope

    print("\n> Person class with properties")

    class Person:
        def __init__(self,name):
            self._name = name

        def getName(self):
            print('> fetch ...')
            return self._name
    
        def setName(self,value):
            print('> change ...')
            self._name = value
        
        def delName(self):
            print("> remove ...")
            del self._name
        
        name = property(getName,setName,delName,'name property docs')
    
    bob = Person('Bob Smith')       # bob has a managed attribute
    print("> initialized Person bob")
    print(f"> > bob - name: {bob.name}")
    print("> change name to Robert Smith")
    bob.name = 'Robert Smith'
    print(f"> > bob - name: {bob.name}")

    print("\n> check _name attr exists")
    print("> > hasattr _name? ",end='')
    print('yes') if hasattr(bob,'_name') else print('no')
    print("> delete attr _name")
    del bob.name
    print("> check _name attr exists")
    print("> > hasattr _name? ",end='')
    print('yes') if hasattr(bob,'_name') else print('no')
    
    print('-'*20)

    sue = Person('Sue Jones')
    print("> initialized Person sue")
    print(f"> > sue - name: {sue.name}")
    print("> change name to Suzanne Jones")
    sue.name = 'Suzanne Jones'
    print(f"> > sue - name: {sue.name}")

    print("\n> properies are inherited (class attrs)")
    class Employee(Person): pass

    tom = Employee('Tom Doe')
    print("> initialized Person tom")
    print(f"> > tom - name: {tom.name}")
    print("> change name to Thomas Doe")
    tom.name = 'Thomas Doe'
    print(f"> > tom - name: {tom.name}")

    print("\n> computed attributes")
    print("> return square with properties")

    class PropSquare:
        def __init__(self,start):
            self.value = start
        
        def getX(self):
            # on attr fetch
            return self.value**2

        def setX(self,value):
            # on attr assign
            self.value = value
        
        X = property(getX,setX)
    
    # Two instances of class with property
    # each has different state information

    P = PropSquare(3)
    print(f"> initialized P with 3: X = {P.X}")

    P.X = 4
    print(f"> changed X to 4: X = {P.X}")

    Q = PropSquare(32)
    print(f"> initialized Q with 32: X = {Q.X}")
    
    print("\n> coding properties with decorators")

    # general syntax:
    # @decorator
    # def func(args): ...
    # is automatically translated to:
    # def func(args): ...
    # func = decorator(func)

    class Person:
        def __init__(self,name):
            self._name = name
        
        @property
        def name(self):
            # name = property(name)
            "name property docs"
            print("> fetch ...")
            return self._name
        
        @name.setter
        def name(self,value):
            # name = name.setter(name)
            print("> change ...")
            self._name = value
        
        @name.deleter
        def name(self):
            # name = name.deleter(name)
            print("> remove ...")
            del self._name
    
    bob = Person('Bob Smith')                   # bob has a managed attribute
    print("> initialized Person bob")
    print(f"> > bob - name: {bob.name}")        # runs name getter
    print("> change name to Robert Smith")
    bob.name = 'Robert Smith'                   # runs name setter
    print(f"> > bob - name: {bob.name}")

def descriptors():
    print("\nDESCRIPTORS")

    # general syntax:
    # class Descriptor:
    #     "docstring goes gere"
    #     def __get__(self,instance,owner): ...   # return attr value
    #     def __set__(self,instance,value): ...   # return None
    #     def __delete__(self,instance): ...      # return None
    
    # self: the descriptor class instance
    # instance: inst. of the client class to which desc. inst. is attached
    # > or None when attr is accessed through the owner class directly
    # owner: the client class to which the descriptor instance is attached

    class Descriptor:
        def __get__(self,instance,owner):
            print("> Descriptor get")
            print(f"> > self: {self}")
            print(f"> > instance: {instance}")
            print(f"> > owner: {owner}")
    
    class Client:
        # Descriptor instance is class attr
        attr = Descriptor()
    
    X = Client()
    print("\n> initialized X as Client()")
    print("> get X.attr:")
    X.attr
    print("> get Client.attr")
    Client.attr

    # fetch X.attr: X.attr -> Descriptor.__get__(Client.attr,X,Client)

    print("\n> read-only descriptors")
    # not enough to omit __set__ because desc. name can be assigned to inst:
    
    print("> store new value for X.attr on Client (99) > hide Descriptor")
    X.attr = 99
    print("> get X.attr:")
    print(X.attr)

    Y = Client()
    print("\n> initialized Y as Client()")
    print("> get Y.attr (still inherits descriptor):")
    Y.attr
    print("> get Client.attr (change not stored on class)")
    Client.attr

    class ReadOnly(Descriptor):
        def __set__(self,instance,value):
            raise AttributeError('cannot set')
    
    class Client:
        # ReadOnly raises error when trying to set
        attr = ReadOnly()
    
    Z = Client()
    print("\n> initialized Z as Client()")
    print("> get Z.attr:")
    Z.attr
    print("> try to set Z.attr: ",end='')
    try:
        Z.attr = 99
    except AttributeError as E:
        print(f"error! {E}")
    
    print("\n> Person class with descriptors")

    class Name:
        "name descriptor docs"
        def __get__(self,instance,owner):
            print("> fetch ...")
            return instance._name
    
        def __set__(self,instance,value):
            print("> change ...")
            instance._name = value
        
        def __delete__(self,instance):
            print('> remove ...')
            del instance._name
    
    class Person:
        def __init__(self,name):
            self._name = name
        # assign descriptor to attr
        name = Name()
    
    bob = Person('Bob Smith')       # bob has a managed attribute
    print("> initialized Person bob")
    print(f"> > bob - name: {bob.name}")
    print("> change name to Robert Smith")
    bob.name = 'Robert Smith'
    print(f"> > bob - name: {bob.name}")

    print("\n> check _name attr exists")
    print("> > hasattr _name? ",end='')
    print('yes') if hasattr(bob,'_name') else print('no')
    print("> delete attr _name")
    del bob.name
    print("> check _name attr exists")
    print("> > hasattr _name? ",end='')
    print('yes') if hasattr(bob,'_name') else print('no')

    print("\n> descriptors are inherited (class attrs)")
    class Employee(Person): pass

    tom = Employee('Tom Doe')
    print("> initialized Person tom")
    print(f"> > tom - name: {tom.name}")
    print("> change name to Thomas Doe")
    tom.name = 'Thomas Doe'
    print(f"> > tom - name: {tom.name}")
            
    print("\n> when descriptor is not useful outside client class")
    print("> it is reasonable to ombed the definition inside client")

    class Person:
        def __init__(self,name):
            self._name = name
            
        class Name:
            "name descriptor docs"
            def __get__(self,instance,owner):
                print("> fetch ...")
                return instance._name
        
            def __set__(self,instance,value):
                print("> change ...")
                instance._name = value
            
            def __delete__(self,instance):
                print('> remove ...')
                del instance._name
        
        name = Name()
    
    print("\n> computed attributes")
    print("> return square with descriptors")

    print("\n> value in descriptor - shared")

    class DescSquare:
        def __init__(self,value):
            self.value = value
        
        def __get__(self,instance,owner):
            # on attr fetch
            return self.value**2
    
        def __set__(self,instance,value):
            # on attr assign
            self.value = value
        
    class Client:
        # Descriptor class attr
        X = DescSquare(2)
        # Class attr
        Y = 3

        def __init__(self):
            # instance attr
            self.Z = 4
        
    C = Client()
    print("> initialized C as Client")
    print(f"> > C.X = {C.X}")
    print(f"> > C.Y = {C.Y}")
    print(f"> > C.Z = {C.Z}")

    C.X = 5
    print(f"> changed X to 5 (intercept): X = {C.X}")
    Client.Y = 6
    print(f"> changed Y to 6 (in class): Y = {C.Y}")
    C.Z = 7
    print(f"> changed Z to 7 (instance): Z = {C.Z}")

    D = Client()
    print("> initialized D as Client")
    print(f"> > D.X = {D.X} < shared! (value in desc)")
    print(f"> > D.Y = {D.Y} < shared! (class attr)")
    print(f"> > D.Z = {D.Z} < not shared ! (per inst)")

    print("\n> value in instance - not shared")

    class ClientSquare:
        def __get__(self,instance,owner):
            # on attr fetch
            return instance._X**2
        
        def __set__(self,instance,value):
            # on attr assign
            instance._X = value
    
    class Client:
        # Descriptor class attr
        X = ClientSquare()
        # Class attr
        Y = 3

        def __init__(self):
            self._X = 2
            self.Z = 4
    
    C = Client()
    print("> initialized C as Client")
    print(f"> > C.X = {C.X}")
    print(f"> > C.Y = {C.Y}")
    print(f"> > C.Z = {C.Z}")

    C.X = 5
    print(f"> changed X to 5 (intercept): X = {C.X}")
    Client.Y = 6
    print(f"> changed Y to 6 (in class): Y = {C.Y}")
    C.Z = 7
    print(f"> changed Z to 7 (instance): Z = {C.Z}")

    D = Client()
    print("> initialized D as Client")
    print(f"> > D.X = {D.X} < not shared! (value in inst)")
    print(f"> > D.Y = {D.Y} < shared! (class attr)")
    print(f"> > D.Z = {D.Z} < not shared ! (per inst)")

    print("\n> descriptor with both data sources")

    class BothSources:
        def __init__(self,data):
            self.data = data
        
        def __get__(self,instance,owner):
            return f"desc: {self.data}, inst: {instance.data}"
        
        def __set__(self,instance,value):
            instance.data = value
    
    class Client:
        def __init__(self,data):
            self.data = data
        
        managed = BothSources('spam')
    
    C = Client('eggs')
    print("> initialized C as Client")
    print(f"> managed attr state: {C.managed}")
    print("> set attr value to SPAM")
    C.managed = 'SPAM'
    print(f"> managed attr state: {C.managed}")
    print("> changes only inst data")

    print(f"\n> no managed in instance dictionary: {C.__dict__}")
    print("> but can access managed with dir and getattr")
    print(f"> > dir: {[x for x in dir(C) if not x.startswith('__')]}")
    print(f"> > getattr (inst. data): {getattr(C,'data')}")
    print(f"> > getattr (managed): {getattr(C,'managed')}")
    print("> > get all attrs and values, including managed:")
    for i in (x for x in dir(C) if not x.startswith('__')):
        print(f"> > > {i} => {getattr(C,i)}")
    
    # the more generic __getattr__ and __getattribute__ tools
    # don't support this functionality - no class level attrs
    # their 'virtual' attr names do not appear in dir results

    print("\n> properties and descrtiptors are strongly related")
    print("> simulating property built-in with a descriptor:")

    class MyProperty:
        def __init__(self,fget=None,fset=None,fdel=None,doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            self.__doc__ = doc
        
        def __get__(self,instance,instancetype=None):
            if instance is None:
                return self
            if self.fget is None:
                raise AttributeError("can't get attribute") 
            return self.fget(instance)
        
        def __set__(self,instance,value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            self.fset(instance,value)
        
        def __delete__(self,instance):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(instance)
    
    class Person:
        def __init__(self,name=None):
            self._name = name
            
        def getName(self):
            print("getName ...")
            return self._name
        
        def setName(self,value):
            print("setName ...")
            self._name = value
        
        name = MyProperty(getName,setName)
    
    bob = Person('Bob Smith')
    print("> initialized Person bob")
    print(f"> > bob - name: {bob.name}")
    print("> change name to Robert Smith")
    bob.name = 'Robert Smith'
    print(f"> > bob - name: {bob.name}")
    print("> try to delete attr name: ",end='')
    try:
        del bob.name
    except AttributeError as E:
        print(f"error! {E}")

def get_attr_mgmt():
    print("\n__GETATTR__ AND __GETATTRIBUTE__")

    # general syntax:
    # def __getattr__(self,name):       # on undef attr fetch
    # def __getattribute__(self,name):  # on all attr fetch
    # def __setattr__(self,name,value): # on all attr assign
    # def __delattr__(self,name):       # on all attr deletion

    print("\n> simple getter (getattr) + setter")

    class Catcher:
        def __getattr__(self,name):
            print(f"... get {name}")
        
        def __setattr__(self,name,value):
            print(f"... set {name} = {value}")
    
    X = Catcher()
    print("> initialized X as Catcher")

    print("> > fetch undef attr 'job': ",end='')
    X.job
    print("> > set undef attr 'pay' to 99: ",end='')
    X.pay = 99

    print("\n> getattribute is called for all attr (undef+def)")

    class Catcher:
        def __init__(self,value):
            print("... init data")
            self.data = value

        def __getattribute__(self,name):
            print(f"... get {name}")
            # X = object.__getattribute__(self,'other')
        
        def __setattr__(self,name,value):
            print(f"... set {name} = {value}")
            # object.__setattr__(self,'other',value)
    
    print("> initialize X as Catcher")
    X = Catcher('spam')

    print("> > fetch def attr 'data': ",end='')
    X.data
    print("> > fetch undef attr 'job': ",end='')
    X.job
    print("> > set def attr 'data' to 99: ",end='')
    X.data = 99
    print("> > set undef attr 'pay' to 99: ",end='')
    X.pay = 99

    print("\n> trace every attr fetch made to another object")
    print("> passed to the wrapper (proxy) class")

    class Wrapper:
        def __init__(self,object):
            self.wrapped = object
        
        def __getattr__(self,attrname):
            print(f"... trace: {attrname}")
            return getattr(self.wrapped,attrname)
    
    X = Wrapper([1,2,3])
    print("> initialized X as Wrapper, wrapped list [1,2,3]")
    print("> > append 4 to list")
    X.append(4)
    print(f"> > wrapped list: {X.wrapped}")

    print("\n> class Person with getattr")

    class Person1:
        def __init__(self,name):
            self._name = name
        
        def __getattr__(self,attr):
            print(f"> get: {attr}")
            if attr == 'name':
                return self._name
            else:
                raise AttributeError(attr)
        
        def __setattr__(self,attr,value):
            print(f"> set: {attr} = {value}")
            if attr == 'name':
                attr = '_name'
            self.__dict__[attr] = value
        
        def __delattr__(self,attr):
            print(f"> del: {attr}")
            if attr == 'name':
                attr = '_name'
            del self.__dict__[attr]
    
    bob = Person1('Bob Smith')
    print("> initialized Person bob")
    print(f"> > bob - name: {bob.name}")
    print("> change name to Robert Smith")
    bob.name = 'Robert Smith'
    print(f"> > bob - name: {bob.name}")
    print("> delete attr name:")
    del bob.name

    print("\n> class Person with getattribute")

    class Person2(Person1):
        
        def __getattribute__(self, attr):
            print(f"> get: {attr}")
            if attr == 'name':
                attr = '_name'
            return object.__getattribute__(self,attr)

        def __getattr__(self,attr):
            self.__getattribute__(self,attr)
    
    sue = Person2('Sue Jones')
    print("> initialized Person sue")
    print(f"> > sue - name: {sue.name}")
    print("> change name to Suzanne Jones")
    sue.name = 'Suzanne Jones'
    print(f"> > sue - name: {sue.name}")
    print("> delete attr name:")
    del sue.name

    print("\n> computed attributes")
    print("> return square with getattr")

    class AttrSquare1:
        def __init__(self,value):
            # triggers __setattr__
            self.value = value
        
        def __getattr__(self,attr):
            if attr == 'X':
                return self.value**2
            else:
                raise AttributeError(attr)
        
        def __setattr__(self,attr,value):
            if attr == 'X':
                attr = 'value'
            self.__dict__[attr] = value
    
    A = AttrSquare1(3)
    print(f"> initialized A with 3: X = {A.X}")

    A.X = 4
    print(f"> changed X to 4: X = {A.X}")

    B = AttrSquare1(32)
    print(f"> initialized B with 32: X = {B.X}")

    print("> return square with getattribute")

    class AttrSquare2(AttrSquare1):

        def __getattribute__(self, attr):
            if attr == 'X':
                return object.__getattribute__(self,'value')**2
                # self.value results in 2x call to getattribute
            else:
                return object.__getattribute__(self,attr)

        def __getattr__(self, attr):
            self.__getattribute__(self,attr)
    
    A = AttrSquare2(3)
    print(f"> initialized A with 3: X = {A.X}")

    A.X = 4
    print(f"> changed X to 4: X = {A.X}")

    B = AttrSquare2(32)
    print(f"> initialized B with 32: X = {B.X}")

    print("\n> getattr and getattribute compared")

    class GetAttr:
        attr1 = 1

        def __init__(self):
            self.attr2 = 2
        
        def __getattr__(self,attr):
            print(f"> get: {attr}")             # not on attr1: inherit from class
            if attr == 'attr3':                 # not on attr2: stored on instance
                return 3
            else:
                raise AttributeError(attr)
    
    X = GetAttr()
    print("\n> X initialized as GetAttr")
    print(X.attr1)
    print(X.attr2)
    print(X.attr3)
    print('_'*20)

    class GetAttribute:
        attr1 = 1

        def __init__(self):
            self.attr2 = 2
        
        def __getattribute__(self,attr):
            print(f"> get: {attr}")
            if attr == 'attr3':
                return 3
            else:
                return object.__getattribute__(self,attr)
    
    X = GetAttribute()
    print("\n> X initialized as GetAttribute")
    print(X.attr1)
    print(X.attr2)
    print(X.attr3)

def attr_mgmt_techniques():    
    print("\nMANAGEMENT TECHNIQUES COMPARED")

    def mgmt_test(mgmt_type):
        X = mgmt_type(3,4)
        print("> init X as Powers: ^2 base = 3, ^3 base = 4")
        print(f"> > {X._square}^2 = {X.square}")
        print(f"> > {X._cube}^3 = {X.cube}")

        print("> set new values: ^2 base = 5, ^3 base = 6")
        X.square = 5
        X.cube = 6
        print(f"> > {X._square}^2 = {X.square}")
        print(f"> > {X._cube}^3 = {X.cube}")

        # base values stored with _x to prevent
        # clashing with names of the properties

    print("\n1. PROPERTIES")

    class PowersProperties:
        def __init__(self,square,cube):
            self._square = square
            self._cube = cube
        
        def getSquare(self):
            return self._square**2
        
        def setSquare(self,value):
            self._square = value
        
        square = property(getSquare,setSquare)
    
        def getCube(self):
            return self._cube**3
        
        def setCube(self,value):
            self._cube = value

        cube = property(getCube,setCube)
    
    mgmt_test(PowersProperties)

    print("\n2. DESCRIPTORS")

    class PowersDescriptors:
        def __init__(self,square,cube):
            self._square = square
            self._cube = cube
        
        class SquareDesc:
            def __get__(self,instance,owner):
                return instance._square**2
            
            def __set__(self,instance,value):
                instance._square = value

        square = SquareDesc()
        
        class CubeDesc:
            def __get__(self,instance,owner):
                return instance._cube**3
        
            def __set__(self,instance,value):
                instance._cube = value

        cube = CubeDesc()
    
    mgmt_test(PowersDescriptors)

    print("\n3A. GETATTR")

    class PowersGetAttr:
        def __init__(self,square,cube):
            self._square = square
            self._cube = cube
        
        def __getattr__(self,name):
            if name == 'square':
                return self._square**2
            elif name == 'cube':
                return self._cube**3
            else:
                raise TypeError(f"unknown attr: {name}")
        
        def __setattr__(self,name,value):
            if name == 'square':
                self._square = value
            elif name == 'cube':
                self._cube = value
            else:
                self.__dict__[name] = value
        
    mgmt_test(PowersGetAttr)

    print("\n3B. GETATTRIBUTE")

    class PowersGetAttribute:
        def __init__(self,square,cube):
            self._square = square
            self._cube = cube
        
        def __getattribute__(self,name):
            if name == 'square':
                return object.__getattribute__(self,'_square')**2
            elif name == 'cube':
                return object.__getattribute__(self,'_cube')**3
            else:
                return object.__getattribute__(self,name)
        
        def __setattr__(self,name,value):
            if name == 'square':
                object.__setattr__(self,'_square',value)
            elif name == 'cube':
                object.__setattr__(self,'_cube',value)
            else:
                object.__setattr__(self,name,value)
        
    mgmt_test(PowersGetAttribute)

def intercept_builtin_op_attr():
    print("\nINTERCEPTING BUILT-IN OPERATION ATTRIBUTES (Ch 32. continued)")

    print("> there is no direct way to to generically intercept built-in ops")
    print("> interface proxies cannot generically intercept o.o. method calls")
    print("> wrappers need to redefine all relevant o.o. methods in themselves")

    def test_attr(get_attr_cls):
        X = get_attr_cls()
        print(f"> 'eggs' stored on class: {X.eggs}")
        print(f"> 'spam' stored on inst: {X.spam}")
        print(f"> 'other' not defined: {X.other}")
        print(f"> __len__ def explicitly: {len(X)}")
        print("> __str__ def via built-in:")
        print(f"... {str(X).strip('<>').split('.')[-1]}")
        
        print("\n> implicit operations fail:")

        print("> > try indexing: ",end='')
        try:
            print(X[0])
        except Exception as E:
            print(f"error! {E}")
        
        print("> > try adding: ",end='')
        try:
            print(X+99)
        except Exception as E:
            print(f"error! {E}")
        
        print("> > try calling: ",end='')
        try:
            print(X())
        except Exception as E:
            print(f"error! {E}")

        print("\n> explicit operations work")

        print("> > call:")
        X.__call__()

        print("> > str (from type):")
        print(f"... {X.__str__().strip('<>').split('.')[-1]}")

    print("\n> GETATTR")

    class GetAttr:
        eggs = 99

        def __init__(self):
            self.spam = 77
        
        def __len__(self):            
            return 42   # else __getattr__ called with __len__
        
        def __getattr__(self,attr):
            print(f'... getattr: {attr}')
            # provide __str__ if asked, else dummy func
            if attr == '__str__':
                return lambda *args: '[GetAttr str]'
            else:
                return lambda *args: None
    
    test_attr(GetAttr)

    print("\n> GETATTRIBUTE")

    class GetAttribute:
        eggs = 88

        def __init__(self):
            self.spam = 66
        
        def __len__(self):
            return 42   # else __getattr__ called with __len__
        
        def __getattribute__(self, attr):
            print(f'... getattribute: {attr}')
            # provide __str__ if asked, else dummy func
            if attr == '__str__':
                return lambda *args: '[GetAttribute str]'
            else:
                return lambda *args: None
    
    test_attr(GetAttribute)

def delegation_mgrs():
    print("\nDELEGATION-BASED MANAGERS REVISITED")

    class Person:
        def __init__(self,name,job=None,pay=0):
            self.name = name
            self.job = job
            self.pay = pay
        
        def lastName(self):
            return self.name.split()[-1]
        
        def giveRaise(self,percent):
            self.pay = int(self.pay*(1+percent))
        
        def __repr__(self):
            return f'[Person: {self.name}, {self.pay}]'
        
    class Manager:
        def __init__(self,name,pay):
            self.person = Person(name,'mgr',pay)    # embed Person object
        
        def giveRaise(self,percent,bonus=0.10):
            self.person.giveRaise(percent+bonus)    # intercept, delegate
    
    sue = Person('Sue Jones',job='dev',pay=100000)
    print("\n> initialized Sue as Person")
    print(sue)
    print(f"> > sue - last name: {sue.lastName()}")
    print("> > give raise 10%")
    sue.giveRaise(0.10)
    print(sue)
    
    class Manager1(Manager):
        def __getattr__(self,attr):
            return getattr(self.person,attr)        # delegate all other attrs
    
    class Manager1A(Manager1):
        def __repr__(self):
            return str(self.person)
            # if we omit __repr__ in wrapper, printing does NOT route its attr fetch
            # through the generic __getattr__ interceptor, inherits object's __repr__

    class Manager2(Manager):
        def __getattribute__(self,attr):
            if attr in ['person','giveRaise']:
                return object.__getattribute__(self,attr)   # fetch my attrs
            else:
                return getattr(self.person,attr)            # delegate all others
    
    class Manager2A(Manager2):
        def __repr__(self):
            person = object.__getattribute__(self,'person')
            return str(person)
            # still have to redefine o.o. explicitly, it doesn't route through interceptor
            # using getattribute instead of getattr doesn't affect the need for redundancy

    def test_mgr(mgr_type):
        tom = mgr_type('Tom Jones',50000)
        print(f"\n> initialized Tom as {mgr_type.__name__}")
        print(tom)
        print(f"> > tom - last name: {tom.lastName()}")   # Manager.__getattr__ > Person.lastName    
        print("> > give raise 10% + bonus")
        tom.giveRaise(0.10)
        print(tom)
    
    for mgr_type in (Manager1,Manager1A,Manager2,Manager2A):
        test_mgr(mgr_type)

def attr_validations():
    print("\nEXAMPLE: ATTRIBUTE VALIDATIONS")

    # CardHolder object with managed attributes which
    # validate or transform values when fetched or stored

    print("\n1. PROPERTIES")

    # note: name mangling - attr assign inside __init___ trigger property setters
    # when this method dassigns to self.name, invokes the setName method which
    # transforms value, assigns to instance attr called __name to avoid clashes
    # data is stored in __name, attr called name is always a property, not data
    # neccessary > properties use common instance state, have none of their own
    
    def test_holder(holder_class):

        def print_holder(who):
            print('-'*30)
            print(f"> account number:   {who.account}")
            print(f"> name:             {who.name}")
            print(f"> age:              {who.age}")
            print(f"(remain to retire:  {who.remain})")
            print(f"> address:          {who.address}")
            print('-'*30)
        
        bob = holder_class('1234-5678','Bob Smith',40,'123 Main St')
        print("> init bob")

        print_holder(bob)

        print("> set bob name to Bob Q. Smith")
        bob.name = 'Bob Q. Smith'
        print("> set bob name to 50")
        bob.age = 50
        print("> set bob account number to 23-45-67-89")
        bob.account = '23-45-67-89'

        print_holder(bob)

        sue = holder_class('5678-1234','Sue Jones',35,'321 Main St')
        print("> init sue")

        print_holder(sue)

        print("> try to set sue age to 100:")
        try:
            sue.age = 100
        except Exception as E:
            print(f"> > Bad age for Sue ({E})")
        
        print("> try to set sue account number to 1234567:")
        try:
            sue.account = '1234567'
        except Exception as E:
            print(f"> > Bad account number for Sue ({E})")
        
        print("> try to manipulate remain value, set to 5: ")
        try:
            sue.remain = 5
        except TypeError as E:
            print(f"> > Error! {E}")

        print_holder(sue)

        print("> bob data still valid?")

        print_holder(bob)

    class CardHolderProperties:
        account_len = 8
        retireage = 59.5

        def __init__(self,account,name,age,address):
            self.account = account
            self.name = name
            self.age = age
            self.address = address
        
        def getName(self):
            return self._name
        def setName(self,value):
            self._name = value.lower().replace(' ','_')
        name = property(getName,setName)

        def getAge(self):
            return self._age
        def setAge(self,value):
            if value < 0 or value > 60:
                raise ValueError('invalid age')
            else:
                self._age = value
        age = property(getAge,setAge)

        def getAccount(self):
            return f"{self._account[:3]}***"
        def setAccount(self,value):
            value = value.replace('-','')
            if len(value) != self.account_len:
                raise TypeError('invalid account number')
            else:
                self._account = value
        account = property(getAccount,setAccount)

        def getRemain(self):
            return self.retireage - self.age
        def setRemain(self,value):
            raise TypeError('cannot set remain')
        remain = property(getRemain,setRemain)

    print("\n2. DESCRIPTORS")
    print("2.1. validating with shared descriptor instance state")

    # note: attr assign inside __init__ trigger descriptor __set__ methods
    # self.name > Name.__set__() > transforms value, assigns to desc. attr name

    class CardHolderDescriptors1:
        account_len = 8
        retireage = 59.5

        def __init__(self,account,name,age,address):
            self.account = account
            self.name = name
            self.age = age
            self.address = address

        class Name:
            def __get__(self,instance,owner):
                return self._name
            def __set__(self,instance,value):
                self._name = value.lower().replace(' ','_')
        name = Name()

        class Age:
            def __get__(self,instance,owner):
                return self._age
            def __set__(self,instance,value):
                if value < 0 or value > 60:
                    raise ValueError('invalid age')
                else:
                    self._age = value
        age = Age()

        class Account:
            def __get__(self,instance,owner):
                return f"{self._account[:3]}***"
            def __set__(self,instance,value):
                value = value.replace('-','')
                if len(value) != instance.account_len:
                    raise TypeError('invalid account number')
                else:
                    self._account = value
        account = Account()

        class Remain:
            def __get__(self,instance,owner):
                return instance.retireage - instance.age
            def __set__(self,instance,value):
                raise TypeError('cannot set remain')
        remain = Remain()

    # problem here is that state stored inside a descriptor itself is
    # class level data, effectively shared by all client class instances
    # cannot vary between them, can only vary per attribute appearence
    # > same in all owner class instances, new values overwrite old ones

    print("2.2. validating with per-client instance state")

    # using same __X naming convention as the property-based equivalent

    class CardHolderDescriptors2:
        account_len = 8
        retireage = 59.5

        def __init__(self,account,name,age,address):
            self.account = account
            self.name = name
            self.age = age
            self.address = address
        
        class Name:
            def __get__(self,instance,owner):
                return instance._name
            def __set__(self,instance,value):
                instance._name = value.lower().replace(' ','_')
        name = Name()
        
        class Age:
            def __get__(self,instance,owner):
                return instance._age
            def __set__(self,instance,value):
                if value < 0 or value > 60:
                    raise ValueError('invalid age')
                else:
                    instance._age = value
        age = Age()

        class Account():
            def __get__(self,instance,owner):
                return f"{instance._account[:3]}***"
            def __set__(self,instance,value):
                value = value.replace('-','')
                if len(value) != instance.account_len:
                    raise TypeError('invalid account number')
                else:
                    instance._account = value
        account = Account()

        class Remain:
            def __get__(self,instance,owner):
                return instance.retireage - instance.age
            def __set__(self,instance,value):
                raise TypeError('cannot set remain')
        remain = Remain()

    print("\n3. GETATTR AND GETATTRIBUTE")
    print("3.1. validating with getattr")

    # note: attr assign inside the __init__ triggers __setattr__ method
    # assign to self.name > invokes __setattr__ > transforms and assigns to name
    # storing name on instance ensures that future access will not trigger __getattr__
    
    class CardHolderGetAttr:
        account_len = 8
        retireage = 59.5

        def __init__(self,account,name,age,address):
            self.account = account
            self.name = name
            self.age = age
            self.address = address
        
        def __getattr__(self,name):
            if name == 'account':
                return f"{self._account[:3]}***"
            elif name == 'remain':
                return self.retireage - self.age
            else:
                raise AttributeError(name)
        
        def __setattr__(self,name,value):
            if name == 'name':
                value = value.lower().replace(' ','_')
            elif name == 'age':
                if value < 0 or value > 60:
                    raise ValueError('invalid age')
            elif name == 'account':
                name = '_account'
                value = value.replace('-','')
                if len(value) != self.account_len:
                    raise TypeError('invalid account number')
            elif name == 'remain':
                raise TypeError('cannot set remain')
            self.__dict__[name] = value
    
    print("3.2. validating with getattribute")

    class CardHolderGetAttribute:
        account_len = 8
        retireage = 59.5

        def __init__(self,account,name,age,address):
            self.account = account
            self.name = name
            self.age = age
            self.address = address

        def __getattribute__(self,name):
            superget = object.__getattribute__
            if name == 'account':
                return f"{superget(self,'account')[:3]}***"
            elif name == 'remain':
                return superget(self,'retireage')-superget(self,'age')
            else:
                return superget(self,name)
        
        def __setattr__(self,name,value):
            if name == 'name':
                value = value.lower().replace(' ','_')
            elif name == 'age':
                if value < 0 or value > 60:
                    raise ValueError('invalid age')
            elif name == 'account':
                value = value.replace('-','')
                if len(value) != self.account_len:
                    raise TypeError('invalid account number')
            elif name == 'remain':
                raise TypeError('cannot set remain')
            self.__dict__[name] = value

    # test_holder(CardHolderProperties)
    # test_holder(CardHolderDescriptors1)
    # test_holder(CardHolderDescriptors2)
    # test_holder(CardHolderGetAttr)
    test_holder(CardHolderGetAttribute)

attr_validations()