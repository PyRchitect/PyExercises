import sys

def stringify(I):
    str_I = str(I).split('.')
    return str_I[0] + (('...'+str_I[-1]) if len(str_I)>1 else '')

def exc_classes():
    print("\nCODING EXCEPTION CLASSES")

    print("> basic hierarchy - exception categories")

    class General(Exception): pass
    class Specific1(General): pass
    class Specific2(General): pass

    def raiser0():
        X = General()
        # raise superclass instance
        raise X

    def raiser1():
        X = Specific1()
        # raise subclass instance
        raise X
    
    def raiser2():
        X = Specific2()
        # raise subclass instance
        raise X

    print("> match General or any subclass of it")
    for func in (raiser0,raiser1,raiser2):
        try:
            func()
        except General as X:
            print(f"\n> caught: {stringify(sys.exc_info()[0])}")
            print("... alternatively:")
            print(f"> caught: {stringify(X.__class__)}")

    # a small number of excs can fit in a tuple
    #   try:
    #       func()
    #   except (General,Specific1,Specific2)
    #       ...
    # for larger hierarchies this becomes cumbersome
    # also, categorizing allows easier future extending

def exc_hierarchies():
    print("\nEXCEPTION HIERARCHIES")

    print("example: numeric programming library")

    # identify things that can go wrong in code:
    class Divzero(Exception): pass  # division by zero
    class Oflow(Exception): pass    # numeric overflow

    # define functions in which excs are appropriately raised:
    def func():
        ...
        raise Divzero()
    
    # when clients use the library, they wrap calls in try stmts
    try:
        func()
    except (Divzero,Oflow):
        ...
    
    # after a while you revise the lib, add another exc protection
    class Uflow(Exception): pass    # numeric underflow

    # now every client needs to update their code to reflect this
    try:
        func()
    except (Divzero,Oflow,Uflow):
        ...    
    # on each lib rev everyone needs to update > bad upgrade policy

    # users could try to avoid this by coding empty catchall clauses
    try:
        func()
    except:
        ...    
    # but now they might catch more than they expected - too general

    # another possibility is to construct and export a tuple of excs
    # containing all excs which could occur in the library
    exc_tuple = (Divzero,Oflow,Uflow)
    # users can load only the tuple, which gets updated with each rev
    try:
        func()
    except exc_tuple:
        ...
    # but you are testing for every exc every time, slows the program

    # > arrange excs into a class tree with a common super (category)
    class NumErr(Exception): pass
    class Divzero(NumErr): pass
    class Oflow(NumErr): pass

    def func():
        ...
        raise Divzero()

    # clients simply list the common super to catch all libs excs
    try:
        func()
    except NumErr:
        ...
    
    # when updating the lib in the future, subclass the common super
    class Uflow(NumErr): pass

    # class excs support state retention and inheritance
    # important in larger programs - maintenance, code reuse

def built_in_exc_classes():
    print("\nBUILT-IN EXCEPTION CLASSES")

    # general hierarchy:
    # BaseException: topmost root, printing and constructor defaults
    # Exception: root of user-defined excs (super of app-related excs)
    # ArithmeticError: root of num errors > Overflow,ZeroDivision,FloatingPoint
    # LookupError: root of indexing errors > Index,Key,Unicode lookup, ...
    # ...

    # Exception class is used as a catchall - allows systems exits and such
    try:
        ...
    except Exception:
        ...
        # handle all app excs
    else:
        ...
        # handle no exc case
    
def print_and_state():
    print("\nDEFAULT PRINTING AND STATE RETENTION")

    def raise_IndexError0(): raise IndexError()    
    def raise_IndexError1(): raise IndexError('spam')        
    
    print("\n> raise IndexError")

    print("> > without args:")
    try:
        raise_IndexError0()
    except Exception as E:
        print(E.__class__)
        print(E.args)
    
    print("> > with args:")
    try:
        raise_IndexError1()
    except Exception as E:
        print(E.__class__)
        print(E.args)
    
    print("> raise custom error")

    class MyExc(Exception): pass

    def raise_MyExc0(): raise MyExc()
    def raise_MyExc1(): raise MyExc('spam','eggs','ham')

    print("\n> raise MyExc")

    print("> > without args:")
    try:
        raise_MyExc0()
    except Exception as E:
        print(E.__class__)
        print(E.args)
    
    print("> > with args:")
    try:
        raise_MyExc1()
    except Exception as E:
        print(E.__class__)
        print(E.args)

def custom_print_disp():
    print("\nCUSTOM PRINT DISPLAYS")

    print("> to provide custom display, use __str__ or __repr__ o.o.")

    class MyBad(Exception):
        def __str__(self):
            return 'Always look on the bright side of life ...'
    
    print("> raise custom exc with str o.o:")
    try:
        raise MyBad()
    except MyBad as X:
        print(X)
    
    # __str__ is preferred to __repr__ in some contexts and the super has it
    # need to o.o. __str__, otherwise super's will be called for i.e. printing

def exc_details():
    print("\nPROVIDING EXCEPTION DETAILS")

    print("> example: data parsing program")

    class FormatError(Exception):
        def __init__(self,line,file):
            # custom constructor, o.o.
            # fills exc with details about the error
            self.line = line
            self.file = file
        
    def parser():
        raise FormatError(42,file='spam.txt')
    
    try:
        parser()
    except FormatError as X:
        print(f"> > Error at: {X.file} ln {X.line}")
    
    print("> alternatively, can rely on super (less specific)")

    class FormatErrorSimple(Exception): pass

    def parser():
        raise FormatErrorSimple(42,'spam.txt')

    try:
        parser()
    except FormatErrorSimple as X:
        print(f"> > Error at: {X.args[1]} ln {X.args[0]}")
    
def exc_methods():
    print("\nPROVIDING EXCEPTION METHODS")

    print("example: data parsing program")

    class FormatErrorLog(Exception):
        logfile = sys.path[0]+'\\'+'logfile.txt'

        def __init__(self,line,file):
            self.line = line
            self.file = file

        def logerror(self):            
            log = open(self.logfile,'a')
            print(f'Error at: {self.file} ln {self.line}',file=log)
    
    def parser():
        raise FormatErrorLog(42, 'spam.txt')
    
    try:
        parser()
    except FormatErrorLog as X:
        X.logerror()

# exc_details()
# exc_methods()