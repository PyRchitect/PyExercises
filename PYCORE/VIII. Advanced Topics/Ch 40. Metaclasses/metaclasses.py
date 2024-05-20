# metaclasses are often optional, we can usually achieve the same effect
# by passing class objects through manager (helper) functions, but they:

# > provide a more formal and explicit structure
# > help ensure we don't forget to augment classes
# > avoid code redundancy (maintenance!) by factoring
# class customization logic into a single location

def test(superclass_choice,metaclass_choice):
    print("\nmaking class")
    class C(superclass_choice,metaclass=metaclass_choice):
        data = 1
        def method(self,arg):
            return self.data + arg
    
    print("\nmaking instance")
    X = C()
    print("data:",X.data,X.method(2))

def stringify(I):
    str_I = str(I).split('.')
    return str_I[0] + (('...'+str_I[-1]) if len(str_I)>1 else '')

def parse_dict(D):
    return {k:stringify(v) for (k,v) in D.items()}

class test_superclass: ...

def metaclass_basics():
    print("\nMETACLASS BASICS")

    print("example: inserting a method into a set of classes")

    class Extras:
        def extra(self,**args): print("extra!")
        def default(self,**args): print("default!")

    # 1. using simple inheritance:
    class Client1(Extras): ...
    class Client2(Extras): ...
    class Client3(Extras): ...

    print("\n> simple inheritance")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # problem: too static - consider the case where classes are augmented
    # in response to choices made at runtime or to specs in a config file

    def required(test=False): return True if test else False

    class Client1: ...
    if required(): Client1.extra = Extras.extra
    else: Client1.extra = Extras.default

    class Client2: ...
    if required(True): Client2.extra = Extras.extra
    else: Client2.extra = Extras.default

    class Client3: ...
    if required(False): Client2.extra = Extras.extra
    else: Client3.extra = Extras.default

    print("\n> if test after class")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # it would be better from a maintenance perspective to isolate the
    # choice logic in a single place. We could route through mgr func:

    def choose_extras(Class,test=False):
        if required(test): Class.extra = Extras.extra
        else: Class.extra = Extras.default

    class Client1: ...
    choose_extras(Client1)

    class Client2: ...
    choose_extras(Client2,True)

    class Client3: ...
    choose_extras(Client3,False)

    print("\n> manager function simple")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # it would be simpler to enforce the augmentation more simply so that
    # the client doesn't need to understand it or deal with it so explicitly
    # > we'd like to be able to insert auto. code at the end of class stmt

    class metaExtras(type):
        def __init__(Class,classname,superclasses,attributedict):
            if required(Class.test): Class.extra = Extras.extra
            else: Class.extra = Extras.default
            type.__init__(Class,classname,superclasses,attributedict)
        
    class Client1(metaclass=metaExtras): test=False
    class Client2(metaclass=metaExtras): test=True
    class Client3(metaclass=metaExtras): test=False

    print("\n> metaclass basic")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # metaclasses vs class decorators (1): overlap in terms of utility and benefit
    # class decorators can augment classes, independent of any created instances
    # their syntax makes their usage explicit and more obvious than mgr func calls

    # suppose we coded the mgr func to return the augmented class:

    def augmentedClass(Class,test=False):
        if required(test): Class.extra = Extras.extra
        else: Class.extra = Extras.default
        return Class

    class Client1: ...
    choose_extras(Client1)

    class Client2: ...
    choose_extras(Client2,True)

    class Client3: ...
    choose_extras(Client3,False)

    print("\n> manager function with class return")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # we could simplify syntax by applying it as class decorator to the class:

    def choose_extras(test=False):
        def augmentedClass(Class):
            if required(test): Class.extra = Extras.extra
            else: Class.extra = Extras.default
            return Class
        return augmentedClass

    @choose_extras()
    class Client1: ...

    @choose_extras(True)
    class Client2: ...

    @choose_extras(False)
    class Client3: ...

    print("\n> class decorators")
    X = Client1(); Y = Client2(); Z = Client3()
    X.extra(); Y.extra(); Z.extra()

    # decorators techically correspond to metaclass __init__,
    # used to initialize newly created classes. Metaclasses have
    # additional customization hooks beyond class initialization
    # and may perform arbitrary class construction tasks

    # Metaclasses have a __new__ method used to create a class
    # which has no direct counterpart in decorators

    # Metaclasses may provide behavior acquired by classes in
    # the form of methods, which has no analogy in decorators

def metaclass_model():
    print("\nMETACLASS MODEL")

    print("\n> classes are instances of type:")
    print(f"> > type([]): {type([])} ; type(type([])): {type(type([]))}")
    print(f"> > type(list): {type(list)} ; type(type): {type(type)}")

    class C: ...
    X = C()

    print(f"\n> type of custom classes and instances:")
    print(f"> > type of class: {type(C)}")
    print(f"> > class of class: {C.__class__}")
    print(f"> > type of inst: {type(X)}")
    print(f"> > class of inst: {X.__class__}")

    print("\n> metaclasses are subclasses of type")

    # type is a class that generates user-defined classes
    # metaclasses are subclasses of the type class
    # class objects are instances of the type class, or a subclass thereof
    # instance objects are generated from a class

    print("\n> class statement protocol")

    # at the end of a class statement and after running all its nested code
    # in a namespace dictionary corresponding to the class's local scope
    # the type object is called to create the class object:
    # class = type(classname, superclasses, attributedict)
    # the type object defines a __call__o.o.m. that runs two other methods
    # type.__new__(typeclass, classname, superclasses, attributedict)
    # type.__init__(class, classname, superclasses, attributedict)

    class Eggs: ...

    class Spam1(Eggs):
        data = 1
        def method(self,arg):
            return self.data + arg
    
    # Python will internally run the nested block and call the type object:    
    # Spam1 = type('Spam1',(Eggs,),{'data':1,'method':method,'__module__':'__main__'})
    X = Spam1()
    print("\n> example: implicit")
    print(f"> > class: {Spam1}")
    print(f"> > inst: {X}")
    print(f"> > class data: {X.data}")
    print(f"> > inst method: {X.method(2)}")
    print(f"> > bases: {Spam1.__bases__}")
    print(f"> > dict:")
    print([(a,v) for (a,v) in Spam1.__dict__.items() if not a.startswith('__')])

    # this can be done explicitly to create a class dynamically:
    Spam2 = type('Spam2',(Eggs,),{'data':1,'method':(lambda x,y: x.data+y)})

    Y = Spam2()
    print("\n> example: explicit")
    print(f"> > class: {Spam2}")
    print(f"> > inst: {Y}")
    print(f"> > class data: {Y.data}")
    print(f"> > inst method: {Y.method(2)}")
    print(f"> > bases: {Spam2.__bases__}")
    print(f"> > dict:")
    print([(a,v) for (a,v) in Spam2.__dict__.items() if not a.startswith('__')])

def metaclass_declaration():
    print("\nDECLARING METACLASSES")

    class Meta(type): ...
    class Eggs: ...
    class Spam(Eggs,metaclass=Meta): ...    # superclasses before metaclass

    # metaclass dispatch:
    
    # the call to create the class object run at the end of the class stmt
    # is modified to invoke the metaclass instead of the type default:

    # X class = type(classname, superclasses, attributedict)
    # > class = Meta(classname, superclasses, attributedict)

    # X type.__new__(typeclass, classname, superclasses, attributedict)
    # > Meta.__new__(typeclass, classname, superclasses, attributedict)

    # X type.__init__(class, classname, superclasses, attributedict)
    # > Meta.__init__(class, classname, superclasses, attributedict)

    class Meta(type):
        def __new__(meta,classname,supers,classdict):
            return type.__new__(meta,classname,supers,classdict)
    
    class Eggs: ...

    class Spam1(Eggs,metaclass=Meta):
        data = 1
        def method(self,arg):
            return self.data + arg
    
    # Python will internally run the nested block and call the type object:    
    # Spam1 = Meta('Spam1',(Eggs,),{'data':1,'method':method,'__module__':'__main__'})
    X = Spam1()
    print("\n> example: implicit")
    print(f"> > class: {Spam1}")
    print(f"> > inst: {X}")

    # this can be done explicitly to create a class dynamically:
    Spam2 = Meta('Spam2',(Eggs,),{'data':1,'method':(lambda x,y: x.data+y)})

    Y = Spam2()
    print("\n> example: explicit")
    print(f"> > class: {Spam2}")
    print(f"> > inst: {Y}")

def metaclass_coding():
    print("\nCODING METACLASSES")

    print("\n1. simple metaclass with new:")

    class MetaOne(type):
        def __new__(meta,classname,supers,classdict):
            print(f"In MetaOne.new: ",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__new__(meta,classname,supers,classdict)
    
    test(test_superclass,MetaOne)

    print("\n2. simple metaclass with new + init:")

    class MetaTwo(type):
        def __new__(meta,classname,supers,classdict):
            print("In MetaTwo.new: ",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__new__(meta,classname,supers,classdict)
    
        def __init__(Class,classname,supers,classdict):
            print("In MetaTwo.init: ",classname,supers,parse_dict(classdict),sep='\n...')
            print("...init class object: ",list(Class.__dict__.keys()))

    test(test_superclass,MetaTwo)

    print("\n3. using simple factory functions")
    # any callable object can be used as a metaclass provided it accepts the
    # arguments passed and returns an object compatible with the intended class

    def MetaFunc(classname,supers,classdict):
        print("In MetaFunc: ",classname,supers,parse_dict(classdict),sep='\n...')
        return type(classname,supers,classdict)

    test(test_superclass,MetaFunc)

    print("\n4. overloading class creation calls with normal classes")
    # a normal class instance can serve as a metaclass too

    class MetaObj:
        def __call__(self,classname,supers,classdict):
            print("In MetaObj.call: ",classname,supers,parse_dict(classdict),sep='\n...')
            Class = self.__New__(classname,supers,classdict)
            self.__Init__(Class,classname,supers,classdict)
            return Class
        
        def __New__(self,classname,supers,classdict):
            print('In MetaObj.new: ',classname,supers,parse_dict(classdict),sep='\n...')
            return type(classname,supers,classdict)
        
        def __Init__(self,Class,classname,supers,classdict):
            print('In MetaObj.init:',classname,supers,parse_dict(classdict),sep='\n...')
            print('...init class object:',list(Class.__dict__.keys()))

    test(test_superclass,MetaObj())

    # we can use normal superclass inheritance to acquire the call interceptor in this model
    # the superclass here is serving essentially the same role as 'type' in terms of dispatch

    print("\n5. using normal inheritance for call interceptor")

    class SuperMetaObj:
        def __call__(self,classname,supers,classdict):
            print("In SuperMetaObj.call: ",classname,supers,parse_dict(classdict),sep='\n...')
            Class = self.__New__(classname,supers,classdict)
            self.__Init__(Class,classname,supers,classdict)
            return Class

    class SubMetaObj(SuperMetaObj):
        def __New__(self,classname,supers,classdict):
            print("In SubMetaObj.new: ",classname,supers,parse_dict(classdict),sep='\n...')
            return type(classname,supers,classdict)

        def __Init__(self,Class,classname,supers,classdict):
            print("In SubMetaObj.init: ",classname,supers,parse_dict(classdict),sep='\n...')
            return type(classname,supers,classdict)

    test(test_superclass,SubMetaObj())

    # it's possible for metaclasses to catch the creation call at the end of a class stmt directly
    # by redefining the type object's __call__ > redefinitions of __new__ and __call__ must be
    # careful to call back to their defaults in type if they mean to make a class in the end

    print("\n6. overloading class creation calls with metaclasses")

    class SuperMeta(type):
        def __call__(meta,classname,supers,classdict):
            print("In SuperMeta.call: ",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__call__(meta,classname,supers,classdict)

        def __init__(Class,classname,supers,classdict):
            print("In SuperMeta.init: ",classname,supers,parse_dict(classdict),sep='\n...')
            print('...init class object:',list(Class.__dict__.keys()))

    class SubMeta(type, metaclass=SuperMeta):
        def __new__(meta,classname,supers,classdict):
            print("In SubMeta.new: ",classname,supers,parse_dict(classdict),sep='\n...')
            return type.__new__(meta,classname,supers,classdict)

        def __init__(Class,classname,supers,classdict):
            print("In SubMeta.init: ",classname,supers,parse_dict(classdict),sep='\n...')
            print('init class object:',list(Class.__dict__.keys()))

    test(test_superclass,SubMeta)

    print("\n*. built-ins vs explicit fetches and calls")

    class SuperMetaTest(type):
        def __call__(meta,classname,supers,classdict):
            print("In SuperMetaTest.call: ",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__call__(meta,classname,supers,classdict)
    
    class SubMetaTest(SuperMetaTest):   # < super is not sub's metaclass
        def __init__(Class,classname,supers,classdict):
            print("In SubMetaTest init: ",classname,supers,parse_dict(classdict),sep='\n...')

    def test_inheritance(super_metaclass,sub_metaclass):
        print(f"> sub meta class: {sub_metaclass.__class__}")
        print(f"> > MRO: {[n.__name__ for n in sub_metaclass.__mro__]}")

        print(f"\n> call sub metaclass: {sub_metaclass.__call__}")
        print("> > explicitly (routes through super):")
        sub_metaclass.__call__(sub_metaclass,'class_test_explicit',(),{})

        print("> > implicitly (does not route through super):")
        sub_metaclass('class_test_implicit',(),{})

    test_inheritance(SuperMetaTest,SubMetaTest)

def inheritance_instance():
    print("\nINHERITANCE AND INSTANCE")

    # KEY POINTS:
    # 1. metaclasses inherit from the type class (usually)
    # 2. metaclass declarations are inherited by subclasses
    # 3. metaclass attrs are not inherited by class instances
    # 4. metaclass attrs are acquired by classes themselves

    print("\n> meta + super + sub:")

    class MetaOne(type):
        def __new__(meta,classname,supers,classdict):
            print("In MetaOne.new: ",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__new__(meta,classname,supers,classdict)
        
        def toast(self):
            return 'toast'

    class Super(metaclass=MetaOne):     # metaclass inherited by subs too
        def Spam(self):                 # MetaOne run twice for two classes
            return 'spam'
    
    class Sub(Super):                   # Superclass: inheritance versus instance
        def Eggs(self):                 # Classes inherit from superclasses
            return 'eggs'               # but not from metaclasses
    
    def test_meta_super_sub(meta_class,super_class,sub_class):
        print("\ntest classes and instances:")
        print(f"> meta: {stringify(meta_class)}")
        print(f"> super: {stringify(super_class)}")
        print(f"> sub: {stringify(sub_class)}")
        X = sub_class()
        print(f"> inst: {stringify(X)}")

        print("\n> > from instance:")
        print("> > > call method inherited from sub:")
        print(X.Eggs)
        print(X.Eggs())
        print("> > > call method inherited from super:")
        print(X.Spam)
        print(X.Spam())
        print("> > > call method inherited from meta:")
        try: print(X.toast)
        except Exception as E: print(E)
        try: print(X.toast())
        except AttributeError as E: print(f"error! {E}")

        print("\n> > from class:")
        print("> > > call method inherited from sub (own):")
        print(sub_class.Eggs)
        print(sub_class.Eggs(X))
        print("> > > call method inherited from super:")
        print(sub_class.Spam)
        print(sub_class.Spam(X))
        print("> > > call method inherited from meta:")        
        print(sub_class.toast)
        print(sub_class.toast())
        print("    * doesn't take instance as argument:")
        try: sub_class.toast(X)
        except TypeError as E: print(f"error! {E}")

    # test_meta_super_sub(MetaOne,Super,Sub)

    print("\n> meta + inst class: attr inheritance")

    class A(type): attr = 1
    class B(metaclass=A): pass

    def meta_class_inst(meta_class,inst_class):
        print("\ntest classes and instances:")
        print(f"> meta class: {stringify(meta_class)}")
        print(f"> inst class: {stringify(inst_class)}")
        inst_class_instance = inst_class()
        print(f"> inst: {stringify(inst_class_instance)}")
        
        # instance of meta acquires its attr but it is not made available
        # for inheritance by its own instances - the acquisition of names
        # by meta instances is distinct from normal inheritance

        print(f"> > inst_class.attr = ",end='')
        try: print(inst_class.attr)
        except AttributeError as E: print(f"error! {E}")
    
        print(f"> > inst_class_instance.attr = ",end='')
        try: print(inst_class_instance.attr)
        except AttributeError as E: print(f"error! {E}")

        print(f"> > is attr in dict of inst_class? {'attr' in inst_class.__dict__}")
    
    # meta_class_inst(A,B)

    print("\n> super + sub class: attr inheritance")

    class A: attr = 1
    class B(A): pass

    def super_sub_class_inst(super_class,sub_class):
        print("\ntest classes and instances:")
        print(f"> super class: {stringify(super_class)}")
        print(f"> sub class: {stringify(sub_class)}")
        sub_class_instance = sub_class()
        print(f"> inst: {stringify(sub_class_instance)}")

        # if meta morphs from meta to super then names inherited from it
        # become availabla to later instances of B, and are located by
        # searching namespace dictionaries in classes in the tree

        print(f"> > sub_class.attr = {sub_class.attr}")

        print(f"> > sub_class_instance.attr = {sub_class_instance.attr}")

        print(f"> > is attr in dict of sub_class? {'attr' in sub_class.__dict__}")

    # super_sub_class_inst(A,B)

    # this is why metaclasses often do their work by manupulating a new class's dict
    # if they wish to influence the behavior of later instance objects

    print("\n> meta/super + sub: inheritance, same attribute")

    class M(type): attr = 1
    class A: attr = 2
    class B(A,metaclass=M): pass

    def meta_super_class_inst_1(meta_class,super_class,sub_class):
        print("\ntest classes and instances:")
        print(f"> meta class: {stringify(meta_class)}")
        print(f"> super class: {stringify(super_class)}")
        print(f"> sub class: {stringify(sub_class)}")
        sub_class_instance = sub_class()
        print(f"> inst: {stringify(sub_class_instance)}")

        print(f"> > sub_class.attr = {sub_class.attr}")

        print(f"> > sub_class_instance.attr = {sub_class_instance.attr}")

        # supers have precedence over metas

    # meta_super_class_inst_1(M,A,B)

    print("\n> meta/super 2x + sub: inheritance, same attribute")

    class M(type): attr = 1
    class A: attr = 2
    class B(A): pass
    class C(B,metaclass=M): pass

    def meta_super_class_inst_2(meta_class,super_class_1,super_class_2,sub_class):
        print("\ntest classes and instances:")
        print(f"> meta class: {stringify(meta_class)}")
        print(f"> super class 1: {stringify(super_class_1)}")
        print(f"> super class 2: {stringify(super_class_2)}")
        print(f"> sub class: {stringify(sub_class)}")
        sub_class_instance = sub_class()
        print(f"> inst: {stringify(sub_class_instance)}")

        print(f"> > sub_class.attr = {sub_class.attr}")

        print(f"> > sub_class_instance.attr = {sub_class_instance.attr}")

        print(f"> MRO (C): {[n.__name__ for n in C.__mro__]}")

        # __dict__ of each class on the MRO (inheritance) is checked first
    
    # meta_super_class_inst_2(M,A,B,C)

    # classes acquire metaclass attributes through their __class__ link in the
    # same way normal instances inherit from classes through their __class___
    # distinction: instance inheritance does not follow a class's __class__,
    # instead restricts its scope to the __dict__ of each class per the MRO

    print("\n> inheritance tree:")

    def inheritance_tree():
        I = C()

        print("> initialized instance of C")
        print(f"> > MRO (C): {[n.__name__ for n in C.__mro__]}")

        print(f"> I.__class__: {stringify(I.__class__)}")              # inheritance: inst class
        print(f"> C.__bases__: {[stringify(x) for x in C.__bases__]}") # inheritance: class supers
        print(f"> C.__class__: {stringify(C.__class__)}")              # inst.acquisition: meta
        print(f"> C.__class__.attr: {stringify(C.__class__.attr)}")    # can get to meta attrs
    
    # inheritance_tree()

def inheritance():
    print("\nINHERITANCE: THE FULL STORY")

    print("\n1. conceptual basis")

    # > the instance inherits from all its classes
    # > the class inherits from both classes and metaclasses
    # > metaclasses inherit from higher metaclasses

    class M1(type): attr1 = 1                   # metaclass inheritance tree
    print("> M1: super meta")
    class M2(M1): attr2 = 2                     # gets __bases__,__class__,__mro__
    print("> M2(M1): sub meta")

    class C1: attr3 = 3                         # superclass inheritance tree
    print("> C1: super")
    class C2(C1,metaclass=M2): attr4 = 4        # gets __bases__,__class__,__mro__
    print("> C2(C1,metaclass=M2): sub")

    I = C2()
    print("> I is instance of C2")

    print("\n> Inheritance:")
    print("> > Instance I inherits from super tree:")
    print(f" > > attr3 = {I.attr3}, attr4 = {I.attr4}")
    print("> Class C2 inherits from both trees: ")
    print(f" > > attr1 = {C2.attr1}, attr2 = {C2.attr2}, attr3 = {C2.attr3}, attr4 = {C2.attr4}")
    print("> Metaclass M2 inherits from super tree:")
    print(f" > > attr1 = {M2.attr1}, attr2 = {M2.attr2}")

    print("\n2. Links:")
    print(f"> > I.__class__: {I.__class__}")
    print(f"> > C2.__bases__: {C2.__bases__}")
    print(f"> > bases tree from C2 mro: {[x.__name__ for x in C2.__mro__]}")

    print(f"> > C2.__class__: {C2.__class__}")
    print(f"> > M2.__bases__: {M2.__bases__}")
    print(f"> > bases tree from M2 mro: {[x.__name__ for x in M2.__mro__]}")

    print(f"> > M2.__class__: {M2.__class__}")

    print("\n3. Route inheritance to the class's meta tree:")
    print(f"> > attr1: {I.__class__.attr1}")
    print(f"> > attr2: {I.__class__.attr2}")

    # inheritance algorithm: simple version
    # - - - - - - - - - - - - - - - - - - -
    # to look up an explicit attribute name:
    # 1. from an instance I: search the inst, then its classes, then its supers
    # a. the __dict__ of instance I
    # b. the __dict__ of all classes on the mro found at I.__class__, L > R
    # 2. from a class C: search the class, then its supers, then its metas
    # a. the __dict__ of all classes on the mro found at C itself, L > R
    # b. the __dict__ of all metas on the mro found at C.__class__, L > R
    # 3. in rule 1&2 give precedence to data descriptors in step b sources
    # 4. in rule 1&2 skip a, begin search at b for built-in operations

    print("\n4: special interaction with data descriptors (those with __set__)")

    class C: ...
    I = C()
    print("\n> (1) initial values:")
    print(f"> > I.__class__: {I.__class__}")
    print(f"> > I.__dict__: {I.__dict__}")

    print("> > assign data to class's dict using keys:")
    I.__dict__['name'] = 'bob'
    print("> > > assigned value bob to attr 'name'")
    print(f"> > I.name: {I.name}")

    I.__dict__['__class__'] = 'spam'
    print("> > > assigned value 'spam' to __class__:")
    print(f"> > I.__class__: {I.__class__} < unchanged!")

    I.__dict__['__dict__'] = {}
    print("> > > assigned value {} to __dict")
    print(f"> > I.__dict__: {I.__dict__} < + assignments")

    print("\n> (2) class with descriptor")

    class D:
        def __get__(self,instance,owner): print('__get__')
        def __set__(self,instance,owner): print('__set__')
    
    class C: d = D()
    I = C()
    
    print("\n> > instance I inherits data descriptor access:")
    print("> > > get: ",end=''); I.d
    print("> > > set: ",end=''); I.d = 1

    print("> > define same name in instance namespace dict:")
    I.__dict__['d'] = 'spam'
    print("> > > get: ",end=''); I.d
    print("> > > set: ",end=''); I.d = 1
    print("> > > doesn't hide data descriptor in class!")

    print("\n> > if this descriptor didn't define a __set__:")

    class D:
        def __get__(self,instance,owner): print('__get__')
    
    class C: d = D()
    I = C()

    print("> > > get: ",end=''); I.d

    print("> > define same name in instance namespace dict:")
    I.__dict__['d'] = 'spam'
    print("> > > get: ",end=''); print(I.d)
    print("> > > hides the name with descriptor in class!")

    # inheritance algorithm: more complete version
    # 1. from an instance I: search the inst, then its classes, then its supers
    # a. the __dict__ of all classes on the mro found at I.__class__, L > R
    # b. if a data descriptor was found in step a, call its __get__ and exit
    # c. else, return a value in the __dict__ of instance I
    # d. else, call a nondata descriptor or return a value found in step a
    # 2. from a class C: search the class, then its supers, then its metas
    # a. the __dict__ of all metas on the mro found at C.__class__, L > R
    # b. if a data descriptor was found in step a, call its __get__ and exit
    # c. else, call desc/return value in the __dict__ of a class in C's own mro
    # d. else, call a nondata descriptor or return a value found in step a
    # 3. in rule 1&2 built-in operations use just step a sources

    print("\n5. the built-ins special case")

    # instances and classes may both be skipped for built-in operations only
    # example: str > built-in | __str__ explicit name equivalent

    class C:
        attr = 1
        def __str__(self): return 'class'
    
    I = C()
    print("\n> built-ins vs explicit:")
    print(f"> > I.__str__: {I.__str__()} < explicit")
    print(f"> > str(I): {str(I)} < built-in")

    I.__str__ = lambda: 'instance'
    print("> changed I.__str__ to lambda func")

    print(f"> > I.__str__: {I.__str__()} < changed!")
    print(f"> > str(I): {str(I)} < not changed!")

    print("\n> normal names:")
    print(f"> > I.attr: {I.attr}")

    I.attr = 2
    print("> changed I.attr to 2")

    print(f"> > I.attr: {I.attr} < changed!")

    print("\n> the same holds true for classes:")

    # explicit names start at the class, built-ins start at its metaclass

    class D(type):
        def __str__(self): return 'D class'
    
    class C(D): ...

    print(f"> > C.__str__(C): {C.__str__(C)} < explicit, super")
    print(f"> > str(C): {str(C)} < built-in, metaclass!")

    class C(D):
        def __str__(self): return 'C class'
    print("> o.o. __str__ in sub")

    print(f"> > C.__str__(C): {C.__str__(C)} < explicit, class")
    print(f"> > str(C): {str(C)} < built-in, meta!")

    class C(metaclass=D):
        def __str__(self): return 'C class'

    print("> use D as C meta")

    print(f"> > C.__str__(C): {C.__str__(C)} < explicit, class")
    print(f"> > str(C): {str(C)} < built-in, user meta!")

    print("\n> all classes inherit from object, including the default type meta")
    # can be non-trivial to know where a name comes from in this model

    # C appears to get a default __str__ from object instad of meta
    # per the first source of class inheritance (own mro)
    # the built-in skips ahead to the metaclass

    print("> use D as C meta, without o.o. __str__")

    class C(metaclass=D): ...

    print(f"> > C.__str__(C): {C.__str__(C)} < explicit, object")
    print(f"> > C.__str__ object: {C.__str__}")
    print(f"> > str(C): {str(C)} < built-in, user meta!")

    print("> mro:")
    p_mro = lambda k: [x.__name__ for x in k.__mro__]
    print(f"> > class C: {p_mro(C)}")
    print(f"> > meta D: {p_mro(D)}")
    print(f"> > type: {p_mro(type)}")

def metaclass_methods():
    print("\nMETACLASS METHODS")

    print("\n1. method inheritance")

    # methods in metas process their instance classes
    # > not instance objects but classes themselves
    
    class A(type):
        def x(cls): print('ax',cls)     # A metaclass (instances = classes)
        def y(cls): print('ay',cls)     # y is overridden by instance B
    
    class B(metaclass=A):
        def y(self): print('by',self)   # normal class (normal instances)
        def z(self): print('bz',self)   # namespace dict holds y and z
    
    print("\n> from class B:")
    print("> > B.x: x acquired from meta")
    print(B.x)
    print("> > B.y: y overridden in class")
    print(B.y)
    print("> > B.z: z defined in class")
    print(B.z)

    I = B()

    print("\n> from instance I:")
    print("> I.x():")
    try: I.x()
    except AttributeError as E: print(f"error! {E}")
    print("> I.y():")
    try: I.y()
    except AttributeError as E: print(f"error! {E}")
    print("> I.z():")
    try: I.z()
    except AttributeError as E: print(f"error! {E}")

    print("\n2. meta vs class methods")

    # meta methods are designed to manage class-level data, like class methods
    # differ in inheritance vsibility, not accessible except through the class

    class A(type):
        def a(cls): cls.x = cls.y + cls.z       # meta method: gets class
    
    class B(metaclass=A):
        y = 11
        z = 22

        @classmethod                            # class method: gets class
        def b(cls): return cls.x

    print("\n> from class B:")
    print("> > B.x: < class data yet to be created on B (with meta method)")
    try: print(B.x)
    except AttributeError as E: print(f"error! {E}")
    print("> > B.a(): < call meta method (visible to class only)")
    B.a()
    print(f"> > B.x: {B.x} < creates class data on B (visible to instances)")

    I = B()

    print("\n> from instance I:")
    print(f"> > I.x = {I.x}")
    print(f"> > I.y = {I.y}")
    print(f"> > I.z = {I.z}")

    print(f"> > I.b(): {I.b()} < class method (sends class, not instance)")
    print("> > I.a(): < try to access through instance")
    try: I.a()
    except AttributeError as E: print(f"error! {E}")

    print("\n3. operator overloading in meta methods")

    # meta methods may also employ o.o. to make built-in ops applicable to
    # their instance classes, they are designed to process classes themselves
    # built-ins skip class, use meta, explicit names search class + meta

    print("\n(1) getitem")

    class A(type):
        def __getitem__(cls,i): return cls.data[i]
    
    class B(metaclass=A):
        data = 'spam'
    
    print("\n> from class B:")
    print(f"> > B.data: {B.data} < class-level attr")
    print(f"> > B[0]: {B[0]} < meta inst names visible to class only")
    print(B.__getitem__)

    I = B()

    print("\n> from instance I:")
    print(f"> > I.data: {I.data} < attr visible to inst")
    print("> > I[0]: < meta inst names not visible to instances")
    try: I[0]
    except TypeError as E: print(f"error! {E}")

    print("\n(2) getattr")

    class A(type):
        def __getattr__(cls,name): return getattr(cls.data,name)
    
    class B(metaclass=A):
        data = 'spam'
    
    print("> from class B:")
    print(f"> > B.data: {B.data} < class-level attr")
    print(f"> > B.upper(): {B.upper()} < runs through getattr")
    print(B.upper)

    I = B()

    print("\n> from instance I:")
    print(f"> > I.data: {I.data} < attr visible to inst")
    print("> > I.upper(): < meta inst names not visible to instances")
    try: I.upper()
    except AttributeError as E: print(f"error! {E}")

    # explicit attrs are routed to the meta __getattr__, but built-ins are not
    # * even though indexing -is- routed to meta __gettitem__ (special case!)

    print("> > reassign data to list [1,2,3]")
    B.data = [1,2,3]
    print("> > explicit normal names are routed to meta getattr:")
    B.append(4)
    print(f"> > > B.append(4): {B.data}")
    print("> > explicit special names are routed to meta getattr:")
    print(f"> > > B.__getitem__(0): {B.__getitem__(0)}")
    print("> > but built-ins skip meta's getattr too (except getitem!)")
    print(f"> > > B[0]: ",end='')
    try: print(B[0])
    except TypeError as E: print(f"error! {E}") 
    print(f"> > > 2*B: ",end='')
    try: print(2*B)
    except TypeError as E: print(f"error! {E}")

def metaclass_instance_mgmt():
    print("\nMETACLASSES MANAGING INSTANCES INSTEAD OF CLASSES")

    # metaclasses vs class decorators (2): overlap in terms of functionality
    # > class decorators rebind class names to the result of a function
    # at the end of a class statement, after the new class has been created
    # > metas work by routing class object creation through an object
    # at the end of a class statement, in order to create the new class
    # > they are often used achieve the same goals in different ways, but:
    # - metas incur extra steps to manage instances (best used for class mgmt)
    # - decos incur extra steps to manage classes (best used for inst mgmt)

    def mc_dec_test(metaclass_type=None,decorator_type=None):

        mc = metaclass_type or type
        dec = decorator_type or (lambda Class: Class)

        @dec
        class Person(metaclass=mc):                     # create Person with Tracer
            def __init__(self,name,hours,rate):         # Wrapper remembers Person
                self.name = name
                self.hours = hours
                self.rate = rate                        # In-method fetch not traced

            def pay(self):
                return self.hours * self.rate

        print("> Person test:")
        print(f"[metaclass: {mc.__name__}]")
        print(f"[decorator: {dec.__name__}]")
        bob = Person('Bob',40,50)
        print("> initialized Person Bob")               # Bob is really a Wrapper
        print(f"> > Bob name: {bob.name}")              # Wrapper embeds a Person
        print(f"> > Bob pay: {bob.pay()}")              # triggers __getattr__

    print("\nEXAMPLE: attribute tracing")
    # prints trace message whenever any normally named attr of a class inst is fetched

    def wrap_class(Class):
        class Wrapper:
            def __init__(self,*args,**kwargs):          # on inst creation
                self.wrapped = Class(*args,**kwargs)    # enclosing scope name

            def __getattr__(self,attr):
                print(f"[Trace: {attr}]")               # catches all but .wrapped
                return getattr(self.wrapped,attr)       # delegate to wrapped obj
        
        return Wrapper

    print("\n(1) class decorator version")
    def DecoTracer(Class):                              # on @decorator
        return wrap_class(Class)

    mc_dec_test(decorator_type=DecoTracer)

    print("\n(2) metaclass version < less straightforward, incurs extra step")
    def MetaTracer(classname,supers,classdict):         # on class creation call
        # must use simple function instead of a class because
        # type subclasses must adhere to obj creation protocols
        Class = type(classname,supers,classdict)        # make client class
        # must manually create the subject class by calling type
        return wrap_class(Class)

    mc_dec_test(metaclass_type=MetaTracer)

    print("\nEXAMPLE: class decorator returning a meta instance")

    class M(type):
        def __new__(meta,classname,supers,classdict):
            print("In M.__new__",meta,classname,supers,parse_dict(classdict),sep='\n...')
            return type.__new__(meta,classname,supers,classdict)
    
    def dec(Class):
        return M(Class.__name__,Class.__bases__,dict(Class.__dict__))
    
    class A:
        x = 1

    print("> creating class B")

    @dec
    class B(A):
        y = 2
        def method(self): return self.x + self.y

    print("> class B attrs:")
    print(f"> > B.x: {B.x}")
    print(f"> > B.y: {B.y}")

    print("> creating instance I")

    I = B()

    print("> inst I attrs:")
    print(f"> > I.x: {I.x}")
    print(f"> > I.y: {I.y}")
    print("> inst I method:")
    print(f"> > x + y = {I.method()}")

    # would be simpler to move meta to first creation step:
    # class B(A, metaclass = M): ...

    print("\nEXAMPLE: metaclass calling decorator")

    def M_inverse(classname,supers,classdict):
        print("In metaclass",classname,supers,parse_dict(classdict),sep='\n...')
        return dec_inverse(type(classname,supers,classdict))
    
    def dec_inverse(Class):
        print("In decorator",Class.__name__,Class.__bases__,dict(Class.__dict__),sep='\n...')
        return Class
    
    class A:
        x = 1

    print("> creating class B")

    class B(A,metaclass=M_inverse):
        y = 2
        def method(self): return self.x + self.y

    print("> class B attrs:")
    print(f"> > B.x: {B.x}")
    print(f"> > B.y: {B.y}")

    I = B()

    print("> inst I of B attrs:")
    print(f"> > I.x: {I.x}")
    print(f"> > I.y: {I.y}")
    print("> inst I method:")
    print(f"> > x + y = {I.method()}")    

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def dec_test(Class):
        print("In decorator",Class.__name__,Class.__bases__,dict(Class.__dict__),sep='\n...')
        return wrap_class(Class)
    
    print("> creating class C")

    @dec_test
    class C(A):
        y = 2
        def method(self): return self.x + self.y
    
    J = C()

    print("> inst J of C attrs:")
    print(f"> > J.x: {J.x}")
    print(f"> > J.y: {J.y}")
    print("> inst J method:")
    print(f"> > x + y = {J.method()}")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

    print("\nEXAMPLE: class whose meta makes it a string")

    def M_func(classname,supers,classdict):
        return 'spam'
    
    class C(metaclass=M_func):
        attr = 'huh?'

    print(f"> class C: {C}")

    print("\nEXAMPLE: class whose decorator makes it a string")

    def dec_func(Class):
        return 'spam'

    @dec_func
    class C:
        attr = 'huh?'
    
    print(f"> class C: {C}")
