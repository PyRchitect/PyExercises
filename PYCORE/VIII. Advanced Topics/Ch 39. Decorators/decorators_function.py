print("CODING FUNCTION DECORATORS")

def add_numbers(first,*rest):
    if not first: return '0'
    
    s_num = first
    s_str = str(first)
    # sum_label = ' + '
    # eq_label = ' = '

    for number in rest:
        s_num += number
        # s_str += sum_label+str(number)
        s_str += f" + {number}"

    # print(s_str + eq_label + str(s_num))
    print(f"{s_str} = {s_num}")

def exp_numbers(base,exp):    
    # exp_label = ' ^ '
    # eq_label = ' = '
    # print(str(base) + exp_label + str(exp) + eq_label + str(base**exp))

    print(f"{base} ^ {exp} = {base**exp}")

def create_tuples(n,d):
    l = []
    for i in range(1,d+1):
        l.append(list(range(i,i+d*n,d)))
    return zip(*l)

def tracing_calls():
    print("\nTRACING CALLS")

    print("\nADD NUMBERS")
    # define and apply a func dec that counts the number of calls
    # made to the dec func and prints a trace message for each call

    test_tuple = (1,2,3)
    print("> TEST 1, without decoration:")

    def add_numbers_1(first,*rest):
        add_numbers(first,*rest)

    add_numbers_1(*test_tuple)

    print("> TEST 2, blank decorator:")

    class tracer_blank:
        def __init__(self,func):
            self.func = func
        
        def __call__(self,*args):
            self.func(*args)

    @tracer_blank
    def add_numbers_2(first,*rest):
        add_numbers(first,*rest)

    add_numbers_2(*test_tuple)

    print("> TEST 3, active decorator:")

    class tracer_active:
        def __init__(self,func):
            self.calls = 0
            self.func = func
        
        def __call__(self,*args):
            self.calls += 1
            print(f"[call #{self.calls}] ",end='')
            self.func(*args)

    @tracer_active
    def add_numbers_3(first,*rest):
        add_numbers(first,*rest)

    add_numbers_3(*test_tuple)

    n = 4; d = 4
    print(f"> > loop calls (n={n},d={d}):")
    for numbers in create_tuples(n,d):
        add_numbers_3(*numbers)
    # total number of calls shows up as an attr of the dec func
    # add_numbers is really an inst of the tracer class when dec
    print(f"> > total calls: {add_numbers_3.calls}")

    print("\n> equivalent without decoration syntax:")

    calls = 0
    def tracer_func(func,*args):
        nonlocal calls
        calls += 1
        print(f"[call #{calls}] ",end='')
        func(*args)
    
    print(f"> > ",end='')
    tracer_func(add_numbers,*test_tuple)
    print(f"> > ",end='')
    add_numbers(*test_tuple)
    print("> > > issue: 'accidental' call without counter")
    print(f"> > ",end='')
    tracer_func(add_numbers,*test_tuple)

def state_ret_op():
    print("\nSTATE RETENTION OPTIONS")

    def add_numbers_test(add_numbers_type):
        print("> add_numbers test")
        test_tuple = (1,2,3)
        test_dict = {'X':1,'Y':2,'Z':3,'flag':'(+)'}

        add_numbers_type(1,2,3)
        add_numbers_type(X=1,Y=2,Z=3,flag='(+)')
        add_numbers_type(*test_tuple)
        add_numbers_type(**test_dict)
        add_numbers_type(1,2,Z=3)
        add_numbers_type(1,2,Z=3,flag='(+)')

    def exp_numbers_test(exp_numbers_type):
        print("> exp numbers test")    
        test_tuple_exp = (2,4)
        test_dict_exp = {'X':2,'Y':4,'flag':'(^)'}
        
        exp_numbers_type(2,4)
        exp_numbers_type(X=2,Y=4,flag='(^)')
        exp_numbers_type(*test_tuple_exp)
        exp_numbers_type(**test_dict_exp)
        exp_numbers_type(2,Y=4)
        exp_numbers_type(2,Y=4,flag='(^)')

    print("\n1. class instance attributes")

    class tracer_kwargs:
        def __init__(self,func):
            self.calls = 0
            self.func = func
        
        def __call__(self,*args,**kwargs):
            self.calls += 1
            print(f"[call #{self.calls}] ",end='')

            # search for and use special keywords pre func call
            if 'flag' in kwargs:
                print(f"(flag: {kwargs['flag']}) ",end='')
                kwargs.pop('flag')

            # forwards filtered keyword args as values to func
            return self.func(*args,*list(kwargs.values()))

    @tracer_kwargs
    def add_numbers_1(first,*rest,**kwargs):
        add_numbers(first,*rest,**kwargs)
    
    add_numbers_test(add_numbers_1)
    
    @tracer_kwargs
    def exp_numbers_1(base,exp):
        exp_numbers(base,exp)

    exp_numbers_test(exp_numbers_1)

    print("\n2. enclosing scopes and globals")

    calls = 0

    def tracer_func_kwargs_GL(func):
        # not really GLobal, only "global" to this tracer
        # unified counter for all calls to tracer
        def wrapper(*args,**kwargs):
            nonlocal calls
            calls += 1
            print(f"[call #{calls}] ",end='')

            # search for and use special keywords pre func call
            if 'flag' in kwargs:
                print(f"(flag: {kwargs['flag']}) ",end='')
                kwargs.pop('flag')

            # forwards filtered keyword args as values to func
            return func(*args,*list(kwargs.values()))

        return wrapper

    @tracer_func_kwargs_GL
    def add_numbers_2(first,*rest,**kwargs):
        add_numbers(first,*rest,**kwargs)
    
    add_numbers_test(add_numbers_2)

    @tracer_func_kwargs_GL
    def exp_numbers_2(base,exp):
        exp_numbers(base,exp)
    
    exp_numbers_test(exp_numbers_2)

    print("\n3. enclosing scopes and nonlocals")

    def tracer_func_kwargs_NL(func):
        # NonLocal to wrapper, inside tracer
        # separate counter for each decorated function
        calls = 0

        def wrapper(*args,**kwargs):
            nonlocal calls
            calls += 1
            print(f"[call #{calls}] ",end='')

            # search for and use special keywords pre func call
            if 'flag' in kwargs:
                print(f"(flag: {kwargs['flag']}) ",end='')
                kwargs.pop('flag')

            # forwards filtered keyword args as values to func
            return func(*args,*list(kwargs.values()))

        return wrapper

    @tracer_func_kwargs_NL
    def add_numbers_3(first,*rest,**kwargs):
        add_numbers(first,*rest,**kwargs)
    
    add_numbers_test(add_numbers_3)

    @tracer_func_kwargs_NL
    def exp_numbers_3(base,exp):
        exp_numbers(base,exp)
    
    exp_numbers_test(exp_numbers_3)

    print("\n4. function attributes")

    def tracer_func_kwargs_FA(func):

        def wrapper(*args,**kwargs):
            wrapper.calls += 1
            print(f"[call #{wrapper.calls}] ",end='')

            # search for and use special keywords pre func call
            if 'flag' in kwargs:
                print(f"(flag: {kwargs['flag']}) ",end='')
                kwargs.pop('flag')

            # forwards filtered keyword args as values to func
            return func(*args,*list(kwargs.values()))
    
        # factory function makes a new function on each call
        # therefore its attributes become per-call state
        wrapper.calls = 0

        return wrapper

    @tracer_func_kwargs_FA
    def add_numbers_4(first,*rest,**kwargs):
        add_numbers(first,*rest,**kwargs)
    
    add_numbers_test(add_numbers_4)

    @tracer_func_kwargs_FA
    def exp_numbers_4(base,exp):
        exp_numbers(base,exp)
    
    exp_numbers_test(exp_numbers_4)

def dec_functions_methods():
    print("\nCLASS BLUNDERS I: DECORATING METHODS")

    def function_test(tracer_label,tracer_type):

        @tracer_type
        def add_numbers_trace(first,*rest,**kwargs):
            add_numbers(first,*rest,**kwargs)

        test_tuple = (1,2,3)
        print(f"> {tracer_label}: function")
        try:
            add_numbers_trace(*test_tuple)
        except TypeError as E:
            print(f"error! {E}")

    def class_test(tracer_label,tracer_type):

        class Person_trace:
            def __init__(self,name,pay):
                self.name = name
                self.pay = pay
            
            @tracer_type
            def give_raise(self,percent):
                self.pay *= (1.0 + percent)
            
            @tracer_type
            def last_name(self):
                return self.name.split()[-1]

        print(f"> {tracer_label}: method")
        bob = Person_trace('Bob Smith',50000)
        print(f"> > initalize bob: {bob.name}, {bob.pay}")

        print("> > give bob 20% raise: ",end='')
        try:
            bob.give_raise(0.20)
            print(bob.pay)
        except TypeError as E:
            print(f"error! {E}")
        
        print("> > give bob 10% raise: ",end='')
        try:
            bob.give_raise(0.10)
            print(bob.pay)
        except TypeError as E:
            print(f"error! {E}")

        print("> > bob last name? ",end='')
        try:
            print(bob.last_name())
        except TypeError as E:
            print(f"error! {E}")

    print("\n1. PROBLEM, ONLY WORKS FOR FUNCTIONS")

    class tracer_basic:
        def __init__(self,func):
            self.calls = 0
            self.func = func
        
        def __call__(self,*args,**kwargs):
            self.calls += 1
            print(f"[call #{self.calls}] ",end='')
            return self.func(*args,*list(kwargs.values()))

    function_test('basic tracer (only for functions)',tracer_basic)
    class_test('basic tracer (only for functions)',tracer_basic)
    
    print("\n2. USING NESTED FUNCTIONS")

    def tracer_func(func):
        calls = 0

        def wrapper(*args,**kwargs):
            nonlocal calls
            calls +=1
            print(f"[Call #{calls}] ",end='')
            return func(*args,*list(kwargs.values()))
    
        return wrapper

    function_test('func tracer',tracer_func)
    class_test('func tracer',tracer_func)

    print("\n3. USING DESCRIPTORS")

    print("\n3.1. EXTERNAL WRAPPERS")

    # add __get__ to tracer to make it a descriptor
    class tracer_desc_external(tracer_basic):
        def __get__(self,instance,owner):
            return wrapper(self,instance)
    
    # need a wrapper class which will route back to tracer call
    class wrapper:
        def __init__(self,desc,subject):
            self.desc = desc
            self.subject = subject
        
        def __call__(self,*args,**kwargs):
            return self.desc(self.subject,*args,**kwargs)

    function_test('desc tracer (external wrapper)',tracer_desc_external)
    class_test('desc tracer (external wrapper)',tracer_desc_external)

    print("\n3.2. EMBEDDED WRAPPERS")

    # add __get__ to tracer to make it a descriptor
    class tracer_desc_embedded(tracer_basic):
        def __get__(self,instance,owner):

            def wrapper(*args,**kwargs):
                return self(instance,*args,**kwargs)

            return wrapper

    function_test('desc tracer (embedded wrapper)',tracer_desc_embedded)
    class_test('desc tracer (embedded wrapper)',tracer_desc_embedded)

    print("\n3.3. REVERSE, ONLY WORKS FOR METHODS")

    class tracer_desc_methods:
        def __init__(self,method):
            self.calls = 0
            self.method = method
        
        def __get__(self,instance,owner):

            def wrapper(*args,**kwargs):
                self.calls += 1
                print(f"[Call #{self.calls}] ",end='')
                return self.method(instance,*args,*list(kwargs.values()))
        
            return wrapper

    function_test('desc tracer (only for methods)',tracer_desc_methods)
    class_test('desc tracer (only for methods)',tracer_desc_methods)
    
def timing_calls():
    print("\nTIMING CALLS")
    import time
    
    def timer_test(timer_type_LC,timer_type_MC):

        import sys
        # force list if python 3:
        force = list if sys.version_info[0]==3 else (lambda X: X)
        
        @timer_type_LC
        def listcomp(N):
            return [x*2 for x in range(N)]
        
        @timer_type_MC
        def mapcall(N):
            return force(map((lambda x: x*2), range(N)))
    
        s = 500; m = 10; n = 5; L = []
        for i in range(n): L.append(s*(m**i))

        print("\n> listcomp:")
        for x in L: listcomp(x)
        print("\n> mapcall:")
        for x in L: mapcall(x)
        print(f"\n> map/comp = {round(mapcall.alltime/listcomp.alltime,2)}")

    print("\n> basic timer version")

    class timer_basic:
        def __init__(self,func):
            self.func = func
            self.alltime = 0
        
        def __call__(self,*args,**kwargs):
            start = time.perf_counter()
            result = self.func(*args,**kwargs)
            elapsed = time.perf_counter() - start
            self.alltime += elapsed
            print(f"> {self.func.__name__}: {elapsed:.5f}, {self.alltime:.5f}")

    # timer_test(timer_basic,timer_basic)

    print("\n> adding decorator args")
    # can use to specify configuration options that can vary for each dec func

    # structure:
    def timer(label=''):
        def decorator(func):
            def onCall(*args):
                ...
                func(*args)
                print(f"{label} ...")
            return onCall
        return decorator
    
    @timer('==>')           # like listcomp = timer('==>')(listcomp)
    def listcomp(N):        # listcomp is rebound to new onCall
        ...

    # listcomp(...)         # really calls onCall

    # adding a label and a trace controle flag to be passed in at dec time
    def timer_args(label='', trace=True):
        class Timer:
            def __init__(self,func):
                self.func = func
                self.alltime = 0
            
            def __call__(self,*args,**kwargs):
                start = time.perf_counter()
                result = self.func(*args,**kwargs)
                elapsed = time.perf_counter() - start
                self.alltime += elapsed

                if trace:
                    print(f"{label} {self.func.__name__}: {elapsed:.5f}, {self.alltime:.5f}")
                
                return result
        return Timer

    timer_test(timer_args(label='[LC]==>'),timer_args(label='[MC]==>'))

    # timer_test(timer_args(label='[LC]',trace=False),timer_args(label='[MC]',trace=False))

def func_dec_vs_mgr_func():
    print("\FUNCTION DECORATORS VS MANAGER FUNCTIONS")

    # function decorators shift special syntax requirements
    # we could simply pass the function and arguments into a
    # manager function that dispatches the call

    # NONDECORATOR VERSION:
    def tracer(func):
        ...
    def func(x,y):
        ...
    result = tracer(func,(1,2))    # special call syntax
    
    # DECORATOR VERSION:
    def tracer(func):
        ...
    @tracer
    def func(x,y):
        ...
    result = func(1,2)             # normal call syntax