# the choice between class dec and metas is arbitrary in many contexts
# it's also possible to use them in combination, as complementary tools

# EXAMPLE: applying a function decorator to all the methods of a class

from types import FunctionType

import time

def tracer(func):
    calls = 0

    def onCall(*args,**kwargs):
        nonlocal calls
        calls += 1
        print(f"[call {calls} to {func.__name__}]")
        return func(*args,**kwargs)

    return onCall

def timer(label='', trace=True):
    def onDecorator(func):
        def onCall(*args,**kwargs):
            start = time.perf_counter()
            result = func(*args,**kwargs)
            elapsed = time.perf_counter() - start
            onCall.alltime += elapsed

            if trace:
                print(f"[{label}{func.__name__}: {elapsed:.5f}, {onCall.alltime:.5f}]")
            
            return result
        
        onCall.alltime = 0
        return onCall
    
    return onDecorator

def person_test(meta_class=None,class_decorator=None):

    # if metaclass not sent, set to default
    # if metaclass sent, assign to mc
    mc = meta_class or type

    # if metaclass not sent, set method dec. to tracer
    # if metaclass sent, set method dec. to do nothing
    md = (lambda x:x) if meta_class or class_decorator else tracer
    # could generalize method dec. to any dec sent, no need    
    # because mc and class decorator solve the problem

    # if class decorator not sent, set to default
    # if metaclass sent, assign to cd
    cd = class_decorator or (lambda x:x)

    @cd
    class Person(metaclass=mc):
        @md
        def __init__(self,name,pay):
            self.name = name
            self.pay = pay        
        @md
        def giveRaise(self,percent):
            self.pay *= (1.0+percent)        
        @md
        def lastName(self):
            return self.name.split()[-1]

    print(f"> metaclass: {mc.__name__}")
    print(f"> class dec: {cd.__name__}")
    print(f"> method dec: {md.__name__}")

    print("- - - TEST - - -")
    bob = Person('Bob Smith',50000)
    print("Initialized Bob as Person")
    print(f"> Bob's name: {bob.name}")

    sue = Person('Sue Jones',100000)
    print("Initialized Sue as Person")
    print(f"> Sue's name: {sue.name}")
    print(f"> Sue's pay: {sue.pay:.2f}")
    print(f"> give Sue 10% raise")
    sue.giveRaise(0.10)
    print(f"> Sue's pay: {sue.pay:.2f}")

def manual_decoration():
    print("\nTRACING WITH DECORATION MANUALLY")

    person_test()

def metaclass_decoration():
    print("\nDECORATING WITH METACLASSES")

    print("\n(1) meta adds tracing dec to every method of client class")

    class MetaTrace(type):
        def __new__(meta,classname,supers,classdict):
            for k,v in classdict.items():
                if type(v) is FunctionType:
                    # metaclass applies the tracing decorator:
                    classdict[k] = tracer(v)
            return type.__new__(meta,classname,supers,classdict)

    person_test(MetaTrace)

    print("\n(2) apply any dec to every method of client class")

    def decorateAll(decorator):
        class MetaDecorate(type):
            def __new__(meta,classname,supers,classdict):
                for k,v in classdict.items():
                    if type(v) is FunctionType:
                        # metaclass applies the decorator from enclosing scope:
                        classdict[k] = decorator(v)
                return type.__new__(meta,classname,supers,classdict)
        return MetaDecorate

    print("\n(2.1) apply tracer")
    person_test(decorateAll(tracer))
    print("\n(2.2) apply timer")
    person_test(decorateAll(timer()))
    print("\n(2.3) apply timer with label")
    person_test(decorateAll(timer(label='**')))

    # tracer, but timer() > timer has an enclosing scope for the decorator
    # tracer: tracer(func) ... return onCall > transforms to onCall(func)
    # timer: timer(...) > onDec(func) ... return onDec > transforms to onDec(...)(func)

def decorator_decoration():
    print("\nDECORATING ALL METHODS WITH FUNC > CLASS DEC")

    def decorateAll(decorator):
        def DecoDecorate(Class):
            for k,v in Class.__dict__.items():
                if type(v) is FunctionType:
                    # decorator applies the decorator from enclosing scope:
                    setattr(Class,k,decorator(v))
            return Class
        return DecoDecorate

    print("\n(1) apply tracer")
    person_test(class_decorator=decorateAll(tracer))
    print("\n(2) apply timer")
    person_test(class_decorator=decorateAll(timer()))
    print("\n(3) apply timer with label")
    person_test(class_decorator=decorateAll(timer(label='**')))

# manual_decoration()
# metaclass_decoration()
# decorator_decoration()