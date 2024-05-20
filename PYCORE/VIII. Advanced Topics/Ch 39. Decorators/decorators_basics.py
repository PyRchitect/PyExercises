# decoration is a way to specify management or augmentation code for functions and classes
# decorators take form of callable objects (functions) that process other callable objects

# there are class and function decorators: they do name rebinding at definition time
# provide a layer of logic, a way to automatically run code at the end of definition stmts

# typical use: augmenting calls to functions and classes by installing wrappers (proxies)
# > call proxies (func. dec.), intercept func. calls, process, pass call to original func.
# > interface proxies (class dec.), intercept inst. creation, process, pass to original class

# alternative use: function and class managers, which manage the objects directly (instead of calls)
# by returning the decorated object instead of a wrapper, they become a simple post-creation step

# f.d. designed to augment only a specific function or method call, not an entire object interface
# c.d. can be used to implement arbitrary object interface augmentation or management tasks

def function_decorators():
    print("\nFUNCTION DECORATORS")

    # general syntax:
    @decorator
    def func(args): ...
    
    # equivalent form:
    def func(args): ...
    func = decorator(func)

    # rebind func name to dec result
    # F(99) > calls decorator(F)(99)

    def decorator(func):
        # process func
        return func

    def decorator(func):
        # save or use func
        save_func = func
        # return a different callable:
        # nested def, class with __call__, ...
        def callable_function(*args):
           ...
        
        return callable_function

    # FUNCTIONS:

    # decorator returns a wrapper which retains the original funcion in enclosing scope
    # when coded this way, each decorated function produces a new scope to retain state
        
    def decorator(func):

        def wrapper(*args):
            save_args = args
            # use func and args
            save_func = func
            # func(*args) calls original function
        
        return wrapper
    
    @decorator
    def func(x,y):
        ...    
    # func = decorator(func) = wrapper      # func is passed to decorator's func    
    # func(6,7) = wrapper(6,7)              # 6,7 (args) are passed to wrapper's args

    # METHODS:
    # we can o.o. the call operation and use instance attrs instead of enclosing scopes
    # when coded this way, each decorated function produces a new inst. to retain state

    class decorator:
        def __init__(self,func):
            self.func = func
        def __call__(self,*args):
            self.save_args = args
            # use self.func and args
            # self.func(*args) calls original function

    @decorator
    def func(x,y):
        ...
    # func = decorator(func)                # func is passed to decorator's __init__
    # func(6,7)                             # 6,7 (args) are passed to __call__'s *args

    # note: class-based solution doesn't work when applied to class-level method functions
    # when coded this way, dec method is rebound to inst of dec class instead of simple func

    class C:
        @decorator
        def method(self,x,y):
            ...
        # method = decorator(method)        # rebound to decorator instance
    
    X = C()
    X.method(6,7)
    
    # in this case self.func(*args) in dec class fails (C instance X is not in args!)
    # to support both functions and methods, the nested function version works better

def class_decorators():
    print("\nCLASS DECORATORS")

    # the decorator's result is what runs when an instance is later created

    # general syntax:
    @decorator
    class C: ...

    # equivalent form:
    class C: ...
    C = decorator(C)

    def decorator(C):
        # process class C
        return C

    def decorator(C):
        # save or use class C
        save_class = C
        # return a different callable:
        # nested def, class with __call__,etc
    
    # callable return by class dec typically creates and returns new instance
    # of the original class, augmented in some way to manage its interface

    # FUNCTIONS:

    def decorator(cls):

        class Wrapper:
            def __init__(self,*args):
                self.wrapped = cls(*args)
            def __getattr__(self,name):
                # intercept undefined attrs
                return getattr(self.wrapped,name)
        
        return Wrapper
    
    @decorator
    class C:
        def __init__(self,x,y):
            # run by Wrapper.__init__
            self.attr = 'spam'
    # C = decorator(C)

    X = C(6,7)          # really calls Wrapper(6,7)
    X.attr              # runs Wrapper.__getattr__ > 'spam'

    # alternative with Wrapper coded outside decorator def:
    class Wrapper: ...

    def decorator(C):
        # on instance creation: new Wrapper
        def onCall(*args):
            # embed instance in instance
            return Wrapper(C(*args))
        return onCall

    # each decorated class creates a new scope which remembers the original class
    # c.d. are commonly coded as factory functions that create and return callables

    # CLASSES:

    class decorator:
        def __init__(self,C):
            self.C = C
        def __call__(self,*args):
            self.wrapped = self.C(*args)
            return self
        def __getattr__(self,attr):
            return getattr(self.wrapped,attr)
        
    X = C()
    Y = C()     # overwrites X
    
    # invalid alt. to f.d: fails to handle multiple instances of a given class
    # each instance creation call overwrites the prior saved instance

def nesting():
    print("\nDECORATOR NESTING")

    # example: coding 2 f.d: 1 to test args before calls, 2 to test returns after calls
    # > can do independently or can nest decorators - result of one is dec func of other

    # multiple nested steps of augmentation > multiple layers of wrapper logic

    def A():
        def wrapper_A():
            ...
        return wrapper_A
    
    def B():
        def wrapper_B():
            ...
        return wrapper_B
    
    def C():
        def wrapper_C():
            ...
        return wrapper_C
    
    # function decorators - general syntax:
    @A
    @B
    @C
    def func(): ...

    # equivalent form:
    def func(): ...
    func = A(B(C(func)))

    # class decorators - general syntax:
    @A
    @B
    @C
    class klass: ...
    X = klass()

    # equivalent form:
    class C: ...
    C = A(B(C(klass)))
    X = C()

    # each dec can return original class or an inserted wrapper object

    # the following do-nothing decorators simply return the dec func:
    def d1(func): return func
    def d2(func): return func
    def d3(func): return func

    @d1
    @d2
    @d3
    def func():
        return 'spam'

    func()  # spam

    # the following concatenates to its result in dec layers as it runs
    def d1(func): return lambda: 'X'+func()
    def d2(func): return lambda: 'Y'+func()
    def d3(func): return lambda: 'Z'+func()

    @d1
    @d2
    @d3
    def func():
        return 'spam'

    func() # XYZspam

    # lambdas used to implement wrapper layers - wrappers can be func, class, ...

def arguments():
    print("\nDECORATOR ARGUMENTS")

    # dec can take args > passed to a callable that returns the dec which returns a callable
    A = 'spam'
    B = 'eggs'

    def decorator(A,B): ...

    @decorator(A,B)
    def func(args): ...
    
    # equivalent form:
    def func(args): ...
    # rebind F to result of decorator's return value
    func = decorator(A,B)(func)
    func(99) # essentially calls decorator(A,B)(F)(99)

    # usually used to retain state information for use in later calls:
    def decorator(A,B):
        # save or use A,B
        def actualDecorator(func):
            # save or use func
            callable = 'spam'
            # return a callable            
            return callable
        return actualDecorator

def managers():
    print("\nDECORATORS MANAGE FUNCTIONS AND CLASSES")

    # decorator mechanism is a protocol for passing functions and classes through any callable
    # immediately after they are created > can be used to invoke arbitrary post-creation processing

    def decorator(O):
        # save or augment function or class O ('O' for object)
        return O

    @decorator
    def func(): ...
    # func = decorator(func)

    @decorator
    class C: ...
    # C = decorator(C)

    # as long as we return the original dec object instead of a proxy
    # we can manage functions and classes themselves, not just later calls