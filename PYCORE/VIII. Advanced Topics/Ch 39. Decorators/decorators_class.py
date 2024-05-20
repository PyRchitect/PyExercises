def singleton_classes():
    print("\nSINGLETON CLASSES")
    # example of managing all instances

    # singleton coding pattern: at most one instance of a class ever exists
    # singleton function defines and returns a function for managing instances
    # @ syntax automatically wraps up a subject class in this function
    
    def Person_singleton_test(singleton_type):

        @singleton_type
        class Person_test:
            def __init__(self,name,hours,rate):
                self.name = name
                self.hours = hours
                self.rate = rate
            
            def pay(self):
                return self.hours * self.rate

        print("\nPERSON CLASS")
        print("> init bob as new Person with singleton decoration")
        bob = Person_test('Bob',40,10)
        print(f"> > name: {bob.name}, pay: {bob.pay()}")

        print("> init sue as new Person with singleton decoration?")
        sue = Person_test('Sue',40,10)
        print(f"> > name: {sue.name}, pay: {sue.pay()}")
        print("> > > cannot create new inst, bob's data remembered")

    def Value_singleton_test(singleton_type):

        @singleton_type
        class Value:
            def __init__(self,value):
                self.value = value
        
        print("\nVALUE CLASS")
        print("> init X with value 42 with singleton decoration")
        X = Value(42)
        print(f"> > X value: {X.value}")
        print("> init Y with value 99 with singleton decoration")
        Y = Value(99)
        print(f"> > Y value: {Y.value}")
        print("> > > cannot create new inst, X's data remembered")

    print("\n0. SETUP - MANAGER FUNCTION")

    instances = {}
    def getInstance(aClass,*args,**kwargs):
        if aClass not in instances:
            instances[aClass] = aClass(*args,**kwargs)
        return instances[aClass]
    
    class Person:
        def __init__(self,name,rate,hours):
            ...
    
    # problem: have to move construction into the manager function
    # each time we want to initialize an instance of managed class
    bob = getInstance(Person,'Bob',40,10)     # vs: bob = Person('Bob',40,10)

    # assuming creating an initial instance is acceptable, we could
    # use introspection to fetch class from an already created inst.

    instances = {}
    def getInstance(object):
        aClass = object.__class__
        if aClass not in instances:
            instances[aClass] = object
        return instances[aClass]

    # problem persists: cannot use normal instance creation syntax
    bob = getInstance(Person('Bob',40,10))    # vs: bob = Person('Bob',40,10)

    print("\n1. USING GLOBAL VARIABLES")

    instances = {}
    def singleton_global(aClass):
        def onCall(*args,**kwargs):
            if aClass not in instances:
                instances[aClass] = aClass(*args,**kwargs)
            return instances[aClass]
        return onCall

    Person_singleton_test(singleton_global)
    Value_singleton_test(singleton_global)

    print("\n2. SELF-CONTAINED ALTERNATIVE")

    def singleton_nonlocal(aClass):
        instance = None
        def onCall(*args,**kwargs):
            nonlocal instance
            if instance == None:
                instance = aClass(*args,**kwargs)
            return instance
        return onCall

    Person_singleton_test(singleton_nonlocal)
    Value_singleton_test(singleton_nonlocal)

    print("\n3. FUNCTION ATTRIBUTES ALTERNATIVE")

    def singleton_attributes(aClass):        
        def onCall(*args,**kwargs):
            if onCall.instance == None:
                onCall.instance = aClass(*args,**kwargs)
            return onCall.instance
        onCall.instance = None
        return onCall

    Person_singleton_test(singleton_attributes)
    Value_singleton_test(singleton_attributes)

    print("\n4. SINGLETON DECORATOR CLASS")

    class singleton_class:
        def __init__(self,aClass):
            self.aClass = aClass
            self.instance = None
        def __call__(self,*args,**kwargs):
            if self.instance == None:
                self.instance = self.aClass(*args,**kwargs)
            return self.instance
    
    Person_singleton_test(singleton_class)
    Value_singleton_test(singleton_class)

def tracing_object_interfaces():
    print("\nTRACING OBJECT INTERFACES")
    # example of augmenting interface of each instance

    # __getattr__ o.o. method can wrap up entire interfaces of embedded instances
    # in order to implement the delegation coding pattern (similar to managed attrs)
    
    # __getattr__ is rune when an undefined attr name is fetched - use as hook
    # intercept method calls in a controller class, propagete to embedded object

    print("\nNON-DECORATED DELEGATION EXAMPLE")

    class Wrapper:
        def __init__(self,object):
            self.wrapped = object
        def __getattr__(self, attr):
            print(f"[Trace: {attr}]")
            return getattr(self.wrapped,attr)
    
    test_object = [1,2,3]
    test_value = 4

    X = Wrapper(test_object)
    print(f"\n> initialized X as Wrapper")
    print(f"> > wrapped object: {X.wrapped}")
    print(f"> > append ({test_value}) through wrapper getattr:")
    X.append(test_value)
    print(f"> > wrapped object: {X.wrapped}")

    test_object = {'a':1,'b':2}
    test_value = {'c':3}

    X = Wrapper(test_object)
    print(f"\n> initialized X as Wrapper")
    print(f"> > wrapped object: {X.wrapped}")
    print(f"> > list object keys: {list(X.keys())}")

    print("\nTRACING INTERFACES WITH CLASS DECORATORS")

    # convenient way to code __getattr__ technique to wrap entire interface

    def tracer_interface_func(aClass):
        class Wrapper:
            def __init__(self,*args,**kwargs):
                self.wrapped = aClass(*args,**kwargs)
                self.calls = 0
            
            def __getattr__(self,attr):
                print(f"[Trace: {attr}]")
                self.calls += 1
                return getattr(self.wrapped,attr)
        return Wrapper

    def Person_interface_test(tracer_type):
        @tracer_type
        class Person_test:
            def __init__(self,name,hours,rate):
                self.name = name
                self.hours = hours
                self.rate = rate
            
            def pay(self):
                return self.hours * self.rate

        print("\nPERSON CLASS")

        print("> init bob as new Person with interface tracking")
        bob = Person_test('Bob',180,20)
        print(f"> > name: {bob.name}, pay: {bob.pay()}")
        
        print("> init sue as new Person with interface tracking")
        sue = Person_test('Sue',160,24)
        print(f"> > name: {sue.name}, pay: {sue.pay()}")

        print(f"> > calls: bob: {bob.calls}, sue: {sue.calls}")
    
    Person_interface_test(tracer_interface_func)

    def Printer_interface_test(tracer_type):
        @tracer_type
        class Printer_test:
            def __init__(self,label,copies):
                self.label = label
                self.copies = copies
            
            def display(self):
                print(self.label*self.copies)
        
        print("\nPRINTER CLASS")

        print("> init spam as new Printer with interface tracking")
        spam = Printer_test('Spam! ',8)
        print(f"> > label: '{spam.label}', copies: {spam.copies}")
        spam.display()

        print("> init eggs as new Printer with interface tracking")
        eggs = Printer_test('Eggs! ',6)
        print(f"> > label: '{eggs.label}', copies: {eggs.copies}")
        eggs.display()
    
        print(f"> > calls: spam: {spam.calls}, eggs: {eggs.calls}")

    Printer_interface_test(tracer_interface_func)
    
    print("\nAPPLYING CLASS DECORATORS TO BUILT-INT TYPES")

    print("\nUSING SUBCLASSING")

    @tracer_interface_func
    class MyList(list): pass

    test_object = [1,2,3]
    test_value = 4

    X = MyList(test_object)
    print("> initialized X as new MyList with interface tracking")
    print(f"> > subclasses list built-in: {X.wrapped}")
    print(f"> > append ({test_value}) through wrapper getattr:")
    X.append(test_value)
    print(f"> > wrapped object: {X.wrapped}")

    print("\nUSING MANUAL DECORATION")

    WrapList = tracer_interface_func(list)
    print("> initialized X as list with interface tracking")
    print(f"> > manually set to route through decorator: {X.wrapped}")
    print(f"> > append ({test_value}) through wrapper getattr:")
    X.append(test_value)
    print(f"> > wrapped object: {X.wrapped}")

    # dec approach allows moving inst creation into dec itself
    # instead of requiring a premade object to be passed in
    # enables retaining normal inst creation syntax and
    # realize all the benefits of decorators in general
    # only need to augment class definition with dec syntax

    def tracer_interface_func(aClass):
        class Wrapper:
            ...
        return Wrapper
    
    class Person: ...

    # DECORATOR APPROACH:
    # bob = Person('Bob',40,50)
    # sue = Person('Sue',rate=100,hours=60)

    # NONDECORATOR APPROACH:
    # bob = Wrapper(Person('Bob',40,50))
    # sue = Wrapper(Person('Sue',rate=100,hours=60))

def retain_multi_inst():
    print("\nCLASS BLUNDERS II: RETAINING MULTIPLE INSTANCES")

    print("\n> alt: dec. function coded as a class")

    class tracer_interface_class:
        def __init__(self,aClass):
            self.aClass = aClass
        
        def __call__(self,*args):
            self.wrapped = self.aClass(*args)
            # ONE (LAST) INSTANCE PER CLASS !
            return self
            # here, objects are really instances of tracer
            # trading enclosing scope for an inst. attr. one
        
        def __getattr__(self,attr):
            print(f"[Trace: {attr}]")
            return getattr(self.wrapped,attr)
    
    @tracer_interface_class
    class Spam:
        def display(self):
            print("Spam! "*8)
    
    @tracer_interface_class
    class Person:
        def __init__(self,name):
            self.name = name
    
    # class-only alt. handles multiple classes as dec. func.
    # doesn't work for multiple instances of a given class
    # each inst. triggers __call__ which overwrites prior inst.

    food = Spam()   # triggers call
    print("> initialized food as Spam inst")
    food.display()  # triggers getattr

    bob = Person('Bob')
    print("> initialized bob as Person inst")
    print(f"> > bob name: {bob.name}")
    sue = Person('Sue')
    print("> initialized sue as Person inst")
    print(f"> > sue name: {sue.name}")
    print(f"> > bob name: {bob.name} < overwritten!")

    # problem is bad state retention - we make 1 dec inst/class,
    # but not 1 dec inst/class inst. > only last inst. retained
    # solution is to abandon class-based dec for this purpose

def class_dec_vs_mgr_func():
    print("\nCLASS DECORATORS VS MANAGER FUNCTIONS")

    # class decorators shift special syntax requirements
    # from the inst creation call to the class stmt itself

    # NONDECORATOR VERSION:
    class Wrapper:
        ...
    class Spam:
        ...
    food = Wrapper(Spam())  # special creation syntax
    
    # DECORATOR VERSION:
    def tracer():
        class Wrapper:
            ...
        return Wrapper
    @tracer
    class Spam:
        ...
    food = Spam()           # normal creation syntax