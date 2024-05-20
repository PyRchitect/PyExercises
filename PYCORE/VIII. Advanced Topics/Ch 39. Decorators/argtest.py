"""
File argtest.py: (3.X + 2.X) function decorator that performs
arbitrary passed-in validations for arguments passed to any
function method. Range and type tests are two example uses;
valuetest handles more arbitrary tests on an argument's value.

Arguments are specified by keyword to the decorator. In the actual
call, arguments may be passed by position or keyword, and defaults
may be omitted. See self-test code below for example use cases.

Caveats: doesn't fully support nesting because call prox args
differ; doesn't validate extra args passed to a decoratee's *args;
and may be no easear than an assert except for canned use cases.
"""

def rangetest(**argchecks):
    return argtest(argchecks,lambda arg,vals: arg<vals[0] or arg>vals[1])

def typetest(**argchecks):
    return argtest(argchecks, lambda arg,type: not isinstance(arg,type))

def valuetest(**argchecks):
    return argtest(argchecks, lambda arg,tester: not tester(arg))

def argtest(argchecks,failif):
    def onDecorator(func):
        if not __debug__:
            return func
        else:
            def onError(argname,criteria):
                raise TypeError(f"{func.__name__} argument '{argname}' not {criteria}")

            def onCall(*pargs,**kwargs):
                code = func.__code__
                expected = list(code.co_varnames[:code.co_argcount])
                positionals = expected[:len(pargs)]

                for (argname,criteria) in argchecks.items():
                    if argname in kwargs:
                        if failif(kwargs[argname],criteria):
                            onError(argname,criteria)
                    elif argname in positionals:
                        position = positionals.index(argname)
                        if failif(pargs[position],criteria):
                            onError(argname,criteria)
                    else:
                        print(f"Argument {argname} defaulted")
                return func(*pargs,**kwargs)
            return onCall
    return onDecorator

if __name__ == '__main__':
    import sys

    def fails(test):
        try: result = test()
        except: print(f"[{sys.exc_info()[1]}]")
        else: print(f"?{result}?")

    print('-'*30) # canned use cases: ranges, types

    @rangetest(m=(1,12),d=(1,31),y=(1900,2013))
    def date(m,d,y):
        print(f"> date: {y}-{m}-{d}")
    
    date(1,2,1960)
    fails(lambda: date(1,2,3))

    @typetest(a=int,c=float)
    def sum(a,b,c,d):
        print(f"... a + b + c + d = {a+b+c+d}")
    
    sum(1,2,3.0,4)
    sum(1,d=4,b=2,c=3.0)
    fails(lambda: sum('spam',2,99,4))
    fails(lambda: sum(1,d=4,b=2,c=99))

    print('-'*30) # arbitrary/mixed tests

    @valuetest(word1=str.islower, word2=(lambda x: x[0].isupper()))    
    def msg(word1='mighty',word2='Larch',label='The'):
        print(f"{label} {word1} {word2}")
    
    msg() # word1 and word2 defaulted
    msg('majestic','Moose')
    fails(lambda: msg('Giant','Redwood'))
    fails(lambda: msg('great',word2='elm'))

    print('-'*30) # manual type and range tests:

    @valuetest(A=lambda x: isinstance(x,int), B=lambda x: x>0 and x<10)
    def manual(A,B):
        print(f"A + B = {A+B}")
    
    manual(100,2)
    fails(lambda: manual(1.99,2))
    fails(lambda: manual(100,100))

    print('-'*30)
    # Nesting: runs both, by nesting proxies on original
    # Open issue: outer levels do not validate positionals due
    # to call proxy function's differing argument signature
    # when trace=True, in all but the last of these "X" is
    # classified as defaulted due to the proxy's signature

    @rangetest(X=(1,10))
    @typetest(Z=str)
    def nester(X,Y,Z):
        return f"{X}-{Y}-{Z}"
    
    print(nester(1,2,'spam'))               # original function runs properly
    fails(lambda: nester(1,2,3))            # nested typetest is run: positional
    fails(lambda: nester(1,2,Z=3))          # nester typetest is run: keyword
    fails(lambda: nester(0,2,'spam'))       # <= outer rangetest not run: positional
    fails(lambda: nester(X=0,Y=2,Z='spam')) # outer rangetest is run: keyword

    print('-'*30)

    class C:
        @rangetest(a=(1,10))
        def meth1(self,a):
            return a*1000
        
        @typetest(a=int)
        def meth2(self,a):
            return a*1000
    
    X = C()
    print(X.meth1(5))
    try: print(X.meth1(20))
    except TypeError as E: print(f"error! {E}")
    print(X.meth2(20))
    try: print(X.meth2(20.9))
    except TypeError as E: print(f"error! {E}")