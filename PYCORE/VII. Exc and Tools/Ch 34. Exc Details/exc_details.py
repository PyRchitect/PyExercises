# try: general form

# try:
    # statements: run this main action first
# except name1:
    # statements: run if name1 is raised during try block
# except (name2,name3):
    # statements: run if any of these exceptions occur
# except nameM as var:
    # statements: run if nameM is raised, assign instance raised to var
# except (nameN,nameP) as var:
    # statements: run if nameN or nameP is raised, combined assign to var
# except Exception:
    # statements: catch all possible exceptions, except exits
# except:
    # statements: run for all other exceptions raised
# else:
    # statements: run if no exception was raised during try block
    # * else block can appear only if there is at least one except
# finally:
    # statements: run regardles of whether an exception occured or not

# raise: general form

# raise
    # reraise the most recent exception
# raise class
    # make and raise instance of class: makes an instance
# raise instance
    # raise instance of class

import os,sys

def default_behavior():
    print("\nDEFAULT BEHAVIOR")

    def divide(x,y): return x/y
    def go_south(x): return divide(x,0)

    X = 1
    print(f"> divide {X}/0: ",end='')
    try:
        print(go_south(1),end=' ')
    except ZeroDivisionError as e:
        print(f"error!\n{e}")

def catching_built_in_exc():
    print("\nCATCHING BUILT-IN EXCEPTIONS")

    def adder(x,y): return x+y
    def conc_str(x): return adder(x,'spam')

    X = [1,2,3]
    print(f"> concatenate {X} and string: ",end='')
    try:
        print(conc_str(X),end=' ')
    except TypeError as e:
        print(f"error!\n{e}")

def try_finally():
    print("\nTRY/FINALLY STATEMENT")    

    class FileExists(Exception):
        def __str__(self):
            return 'file already exists!'

    def write_to_file(filepath,data):
        
        if not os.path.isfile(filepath):
            print("opening file for writing...")
            file = open(filepath,'w')
            try:
                file.write(data)
            finally:
                print("...closing file")
                file.close()
        else:
            raise FileExists()
    
    data = 'SPAM!'

    filepath = sys.path[0]+'\\'+'data.txt'

    print("try to write to file ...")
    try:
        write_to_file(filepath,data)
    except FileExists as e:
        print(f"error! {e}")
    else:
        print("success!")

def try_except_finally():
    print("\nUNIFIED TRY/EXCEPT/FINALLY")

    sep = '-'*45

    print(sep)
    print("EXCEPTION RAISED AND CAUGHT")
    try:
        X = 'spam'[99]
    except IndexError:
        print("except run")
    finally:
        print("finally run")
    print("after run")
    
    print(sep)
    print("NO EXCEPTION RAISED")
    try:
        X = 'spam'[3]
    except IndexError:
        print("except run")
    finally:
        print("finally run")
    print("after run")

    print(sep)
    print("NO EXCEPTION RAISED, WITH ELSE")
    try:
        X = 'spam'[3]
    except IndexError:
        print("except run")
    else:
        print("else run")
    finally:
        print("finally run")
    print("after run")        
    
    print(sep)
    print("EXCEPTION RAISED BUT NOT CAUGHT")
    try:
        X = 1/0
    except IndexError:
        print("except run")
    finally:
        print("finally run")
    print("after run")

def raise_statement():
    print("\nTHE RAISE STATEMENT")

    # raise instance        # raise instance of class
    # raise IndexError()

    # raise class           # make and raise instance of class: makes an instance
    # raise IndexError
    
    # raise                 # reraise the most recent exception

    def create_inst_ahead():
        
        exc = IndexError()
        raise exc
    # create_inst_ahead()

    def create_list_of_inst():

        excs = [IndexError,TypeError]
        raise excs[0]
    # create_list_of_inst()

    def custom_exc_with_args():

        class MyExc(Exception): pass
        raise MyExc('spam')
    # custom_exc_with_args()

    print("\n> scopes and try except variables")
    print("> > exc ref name is localized to the except block")
    print("> > var is actually removed, not reverted to previous value")

    X = 99
    print(f"> > > X value assigned before try/except block: {X}")

    try:
        1/0
    except Exception as X:
        print(f"> > > 1/0, exc raised (used 'as X' to collect args): {X}")
    
    print("> > > X value after except: ",end="")
    
    try:
        print(X)
    except Exception as Y:
        print(Y)

    print("> > different behaviour than with comps")

    X = 99
    print(f"> > > X value assigned before comp: {X}")
    print(f"> > > collect 'spam' in set: ",end="")
    print({X for X in 'spam'})
    print(f"> > > X value after comp: {X}")

    print("> > can save to a different var which won't be removed")

    try:
        1/0
    except Exception as X:
        print(f"> > > 1/0, exc raised (used 'as X' to collect args): {X}")
        exc_save = X
    
    print(f"> > > saved value after except: {exc_save}")

    print("\n> propagating exceptions with raise")
    print("> > raise without exc name or extra data reraises the current exc")
    print("> > used if need to catch an exc, don't want it to die")

    def propagate_exc():

        try:
            raise IndexError('spam')
        except IndexError:
            print("reraise most recent exc, propagate to higher handler:")
            raise

    # propagate_exc()

    print("\n> exception chaining: raise from")
    print("> > triggering exceptions in response to other exceptions")
    # general form: raise NewException from OtherException
    # exp following 'from' specifies another exc attached to the __cause__ attr

    def exc_chain():

        try:
            1/0
        except Exception as E:
            raise TypeError('Bad') from E
    
    # exc_chain()

    print("> > the causallity chain can be arbitrarily long")

    def exc_chain_long():

        try:
            try:
                raise IndexError()
            except Exception as E:
                raise TypeError() from E
        except Exception as E:
            raise SyntaxError() from E
    
    # exc_chain_long()

    print("> > chained exc suppression: raise exc from None")
    print("> > > allows disabling the display of the chained exc context")

def assert_statement():
    print("\nTHE ASSERT STATEMENT")

    print("> the 'conditional' raise statement")

    # general form: assert test, data
    
    # syntactic shorthand for:
    # if __debug__:
    #     if not test:
    #         raise AssertionError(data)

    # __debug__ flag: built-in name, set to True unless -0 flag is used
    # > python -0 main.py -> skip assertions, removed from byte code

    # the data part is optional, appears as part of the std. err. msg.
    # > if provided: exception's constructor argument    

    def f(x):

        assert x<0, 'x must be negative'
        return x**2
    
    print("> > example: return x squared if input negative, else error:")
    print(f"> > > x = -1: ",end='')
    print(f(-1))    
    print(f"> > > x = 1: ",end='')
    try:
        print(f(1))
    except AssertionError as E:
        print(f"error! ({E})")

    print("\n> intended for trapping user-def. constraints, not for catching errors")
    print("> Python traps errors itself, no need to use assert to check explicitly")

    def reciprocal(x):

        assert x!=0, 'must not divide by zero!' # generally useless assert
        return 1/x                              # Python checks for zero itself
    
    print("> > reciprocal, asserts x!=0 > displays ass.error instead of zero div.")
    print(f"> > > x = 1: ",end='')
    print(reciprocal(1))
    print(f"> > > x = 0: ",end='')
    try:
        print(reciprocal(0))
    except AssertionError as E:
        print(f"error! ({E})")
    print(f"> > > 1/0, x = 0: ",end='')
    try:
        print(1/0)
    except ZeroDivisionError as E:
        print(f"error! ({E})")

def with_as_context_mgr():
    print("\nWITH/AS CONTEXT MANAGERS")

    print("> alternative to a common try/finally usage idiom")
    print("> intended for specifying termination-time (cleanup) activities")
    print("> unlike try/finally, it is based upon an object protocol")

    # basic format:
    # with expression [as variable]:
    #     with-block

    # exp is assumed to return an object that supports the context mgmt protocol

    print("\n> example: reading from file")
    filepath = sys.path[0]+'\\'+'data.txt'

    print("> > context mgmt guarantees file is closed after with stmt has run")
    print("> > even if an exception was raised while processing the file")

    with open(filepath) as myfile:
        for line in myfile:
            print(line)    
    
    print("> > similar effect with try/finally (more general and explicit):")

    myfile = open(filepath)
    try:
        for line in myfile:
            print(line)
    finally:
        myfile.close()
    
    print("\n> example: decimal context")
    print("> > uses context mgmt to simplify work with rounding and precision")
    
    import decimal

    with decimal.localcontext() as ctx:
        ctx.prec = 2
        x = decimal.Decimal('1.00') / decimal.Decimal('3.00')
        print(f"> > > 1/3, precision = 2: {x}")
        ctx.prec = 4
        y = decimal.Decimal('1.00') / decimal.Decimal('3.00')
        print(f"> > > 1/3, precision = 4: {y}")
        ctx.prec = 6
        z = decimal.Decimal('1.00') / decimal.Decimal('3.00')
        print(f"> > > 1/3, precision = 6: {z}")
    
    print("\n> after the stmt runs, contex mgr is auto restored to before the stmt")
    print("> to to the same with try/finally, would require manual save > restore")

    print("\n> implementing custom context mgrs with o.o.")

    class TraceBlock:
        def message(self, arg):
        
            print(f"...running {arg}")
        
        def __enter__(self):            
        
            print("\n...starting with block")
            return self
            # return value assigned to the var in the as clause if present
        
        def __exit__(self,exc_type,exc_value,exc_tb):
            # if with block raises an exc, __exit__ is called with exc details
            # if no exc was raised, __exit__ is called with all args set to None
            # args: same 3 values returned by sys.exc_info: type, value, traceback
        
            if exc_type is None:
                print("...exited normally")
            else:
                print(f"...raise an exception! {str(exc_type)}")
                # return False
                # > propagate the exception
                # > or delete the return stmt so that it
                # > > returns None, False by definition
        
    try:
        with TraceBlock() as action:
            action.message('test 1')
    except:
        print("error!")
    else:
        print("success!")

    try:
        with TraceBlock() as action:
            action.message('test 2')
            raise TypeError()
    except:
        print("error!")
    else:
        print("success!")
    
    print("\n> multiple context managers")
    print("> with stmt may specify 'nested' context mgrs with comma syntax")

    # with A() as a, B() as b:
    # ... stmts ...
    # is equivalent to:
    # with A() as a:
    #     with B() as b:
    #     ... stmts ...

    print("\n> example: reading from file and writing to file")
    filepath_in = sys.path[0]+'\\'+'data.txt'
    filepath_out = sys.path[0]+'\\'+'res.txt'

    if not os.path.isfile(filepath_out):
        try:
            with open(filepath_in) as fin, open(filepath_out,'w') as fout:
                for ix,line in enumerate(fin):
                    if 'S' in line:
                        fout.write(f"found 'S' in line {ix}")
        except:
            print("> > error while writing the result file!")
        else:
            print("> > result file written successfully!")
    else:
        print("> > result file already exists!")

    print("\n> example: parallel reading and comparison")
    filepath_t1 = sys.path[0]+'\\'+'test1.txt'
    filepath_t2 = sys.path[0]+'\\'+'test2.txt'

    with open(filepath_t1) as t1, open(filepath_t2) as t2:
        for (ix,(l1,l2)) in enumerate(zip(t1,t2)):
            print(f"ln {ix}\t{l1.strip()}\t{l2.strip()}\t",end='')
            if l1!=l2:
                print("< differ")
            else:
                print("< equal")
    
    print("> not very useful here because files autoclose")

    print("\n> example: autoclose output file on stmt exit")
    print("> ensure buffered text is transferred to disk immediately")


    filepath_in = sys.path[0]+'\\'+'test.txt'

    print("> > 1) using with block")
    filepath_out = sys.path[0]+'\\'+'test_upper_1.txt'

    if not os.path.isfile(filepath_out):
        with open(filepath_in) as fin, open(filepath_out,'w') as fout:
            for line in fin:
                fout.write(line.upper())
    else:
        print("> > converted file already exists!")

    print("> > 2) using try/finally block")
    filepath_out = sys.path[0]+'\\'+'test_upper_2.txt'

    if not os.path.isfile(filepath_out):
        fin = open(filepath_in)
        fout = open(filepath_out,'w')
        try:
            for line in fin:
                fout.write(line.upper())
        finally:
            # close files after processing
            fin.close()
            fout.close()
    else:
        print("> > converted file already exists!")

    print("> > 3) without any block")
    filepath_out = sys.path[0]+'\\'+'test_upper_3.txt'

    if not os.path.isfile(filepath_out):
        fin = open(filepath_in)
        fout = open(filepath_out,'w')
        for line in fin:
            fout.write(line.upper())
    else:
        print("> > converted file already exists!")
    
    print("\n> with/as and try/finally are useful when exc catching is needed")

# default_behavior()
# catching_built_in_exc()
# try_finally()
# try_except_finally()
# raise_statement()
# assert_statement()
# with_as_context_mgr()