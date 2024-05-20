import sys

def control_flow_nesting():
    print("\nCONTROL-FLOW NESTING")

    print("\n> try action1 (outer) > try action2 (inner) > exception!")
    print("> if outer doesn't re-raise, only inner exc is executed")    

    def action2():
        # coded to trigger an exception
        print(1+[])
    
    def action1():
        try:
            action2()
        except TypeError:
            # most recent matching try
            print("...inner try")
    
    try:
        action1()
    except TypeError:
        # here only if action1 re-raises
        print("...outer try")

    print("\n> syntactic nesting - tries inside tries")
    print("> if nested doesn't re-raise, only inner exc is executed")

    try:
        try:
            action2()
        except TypeError:
            # most recent matching try
            print("...inner try")
    except TypeError:
        # here only if nested handler re-raises
        print("...outer try")

    print("\n> nested finally handlers")
    print("> all fire on an exception")

    try:
        try:
            try:
                action2()
            finally:
                print("...inner try")
        finally:
            print("...outer try")
    except:
        print("...exc wrap")

    print("\n> example: catch an exception if one is raised")
    print("> perform a finally termination-time action regardless")

    def raise1(): raise IndexError
    def noraise(): return
    def raise2(): raise SyntaxError

    for func in (raise1,noraise,raise2):
        print(f"<{func.__name__}>")

        try:
            try:
                try:
                    func()
                except IndexError:
                    print("...caught IndexError")
            finally:
                print("...finally run")
            print("...")
        except:
            print("...exc wrap")

def multi_nested_loop_break():
    print("\nBREAKING OUT OG MULTIPLE NESTED LOOPS")

    print("\n> loop1 > loop2 > loop3 > exc break all")

    class ExitLoop(Exception): pass

    try:
        while True:
            while True:
                for i in range(10):
                    if i>3: raise ExitLoop
                    print(f"loop3: {i}")
                print("loop2")
            print("loop1")
    except ExitLoop:
        print("continuing")

def exc_vs_err():
    print("\nEXCEPTIONS AREN'T ALWAYS ERRORS")

    print("> all err are exc, but not all exc are err")
    print("> using EOFError exception as an input signal")

    while True:
        try:
            line = input()
            # EOF: Ctrl+Z-Return
        except EOFError:
            print("input: EOF ... break")
            break
        else:
            print(f"input: {line}")
    
    # similar exc signals:
    # sys.exit() > SystemExit
    # Ctrl+C > KeyboardInterrupt

def non_err_conditions_signals():
    print("\nFUNCTIONS CAN SIGNAL CONDITIONS WITH RAISE")

    print("\n> user-defined exceptions can signal non-error conditions")
    print("> example: searcher which raises 'found' exc if matched element")

    class Found(Exception): pass

    def searcher(list,el):
        matched = True if el in list else False       

        if matched:
            # raise exc instead of returning flags
            raise Found()
        else:
            return

    print("> > is 5 in [0...9]? ",end='')

    try:
        searcher(list(range(10)),5)
    except Found:
        print("...success!")
    else:
        print("...failure")

    print("\n> exc provide a way to signal results without a return value")
    print("> example: searcher which raises 'not found' exc if not matched element")

    class NotFound(Exception): pass

    def searcher(list,el):
        matched = True if el in list else False       

        if matched:            
            return
        else:
            raise NotFound()

    print("> > is 20 in [0...9]? ",end='')

    try:
        searcher(list(range(10)),20)
    except NotFound:
        print("...failure!")
    else:
        print("...success!")

def debug_with_tries():
    print("\nDEBUGGING WITH OUTER TRY STATEMENTS")

    def run_program():
        raise TypeError

    try:
        run_program()
    except:
        # to see what exc occured, fetch sys.exc_info function:
        print(f"> uncaught! {sys.exc_info()[0]} {sys.exc_info()[1]}")

def in_process_tests():
    print("\nRUNNING IN-PROCESS TESTS")

    # in test module:
    def moreTests(): pass
    def testName(): pass
    def runNextTest(): pass
    # from testapi import moreTests,testName,runNextTest

    log = open('testlog','a')

    def test_driver():
        while moreTests():
            try:
                runNextTest()
            except:
                print(f"FAILED {testName()} {sys.exc_info()[:2]}",file=log)
            else:
                print(f"PASSED {testName()}",file=log)

    test_driver()

def about_sys_exc_info():
    print("\nSYS.EXC_INFO")

    # allows an exc handler to gain access to the most recently raised exc
    # useful when using empty except as catchall to determine what was raised

    try:
        ...
    except:
        print(sys.exc_info()[0:2])  # exc class and instance
    
    # if no exc, call returns (None,None,None)
    # otherwise returns (type,value,traceback)

    # can be used to determine exc type when catching superclasses
    # redundant because can get exc type by fetching __class__ attr

    class General(Exception):
        def method(self): print(self.__class__)
    class Specific1(General): pass
    class Specific2(General): pass

    try:
        ...
    except General as instance:
        print(instance.__class__)   # exc class equivalent

    # better approach: using instance object's interfaces and polymorphism

    try:
        ...
    except General as instance:
        instance.method()

def disp_err_traceback():
    print("\nDISPLAYING ERRORS AND TRACEBACKS")

    import traceback

    def inverse(x): return 1/x

    fp = sys.path[0]+'\\'+'badly.exc'
    try:
        inverse(0)
    except Exception:
        traceback.print_exc(file=open(fp,'w'))
    print("Bye!")

def catching_too_much():

    print("> sometimes we need an early termination")
    print("> Python provides sys.exit(statuscode)")
    print("> this works by raising SystemExit exc")

    def bye():
        # crucial error: abort now!
        sys.exit(40)
    
    print("\n> > except catchall")
    try:
        bye()
    except:
        # we prevented the exit
        print('... got it')
    print("continuing ...")

    print("\n> catch exceptions")
    try:
        bye()
    except Exception:
        # exit is allowed (not sub of Exc)
        # super above all built-in excs
        print('... got it')
    print("continuing ...")

    print("\n> could catch programming errors")
    print("> silently continues, debug problems")
    print("> be as specific as possible")

def catching_too_little():
    
    print("> exc catches only what is in exc list")

    class exc1(Exception): pass
    class exc2(Exception): pass

    try:
        ...
    except (exc1,exc2):
        ...
    
    print("> if we add exc3 in the future")

    class exc3(Exception): pass
    
    print("> without updating code it doesn't get caught")

    print("> we can solve this using superclasses")

    class exc_base(Exception): pass
    class exc1(exc_base): pass
    class exc2(exc_base): pass

    try:
        ...
    except exc_base:
        ...

    print("> also catches all subclasses of exc_base")

    print("> more future proof - if we need to rev the lib")
    


# control_flow_nesting()
# multi_nested_loop_break()
# exc_vs_err()
# non_err_conditions_signals()
# debug_with_tries()
# disp_err_traceback()