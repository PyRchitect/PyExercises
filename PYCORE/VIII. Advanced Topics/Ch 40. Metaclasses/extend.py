# compare metaclass and decorator-based implementations of
# class augmentation and instance wrapping

def eggsfunc(obj): return obj.value * 4

def hamfunc(obj,value): return value + 'ham'

def mc_dec_test(metaclass_type=None,decorator_type=None):

    mc = metaclass_type or type
    dec = decorator_type or (lambda Class: Class)

    @dec
    class Client1(metaclass=mc):
        def __init__(self,value):
            self.value = value
        def spam(self):
            return self.value * 2
    
    @dec
    class Client2(metaclass=mc):
        value = 'ni?'
    
    if not any([metaclass_type,decorator_type]):
        print("* meta/deco not provided, using defaults...")
        Client1.eggs = eggsfunc
        Client1.ham = hamfunc

        Client2.eggs = eggsfunc
        Client2.ham = hamfunc

    print("> Client 1 test:")
    X = Client1('Ni!')
    print(f"> > spam method (returns 2*input): {X.spam()}")
    print(f"> > eggs method (returns 3/4/5*input): {X.eggs()}")
    print(f"> > ham method (input +'ham'): {X.ham('bacon')}")

    print("> Client 2 test:")
    Y = Client2()
    print(f"> > eggs method (returns 3/4/5*input): {Y.eggs()}")
    print(f"> > ham method (input +'ham'): {Y.ham('bacon')}")

def manual_augmentation():
    print("\nMANUAL AUGMENTATION")

    # simple class-based inheritance suffices if the extra methods
    # are statically known at the time the class is coded
    # for more dynamic scenarios metaclasses provide an explicit structure
    # and minimize the maintenance cost of changes in the future

    print("\n> manual extender")

    # add two methods to two classes after they have been created
    mc_dec_test()

    # methods can always be assigned to a class after it's been created
    # as long as they are functions with extra first arg for inst (self)
    # manual approach has a major donwside - need to augment every class
    # that needs the methods which we want to add, this is error-prone

def meta_augmentation():
    print("\nMETACLASS-BASED AUGMENTATION")

    print("\n> basic extender")
    
    class Extender(type):
        def __new__(meta,classname,supers,classdict):
            classdict['eggs'] = eggsfunc
            classdict['ham'] = hamfunc
            return type.__new__(meta,classname,supers,classdict)

    mc_dec_test(metaclass_type=Extender)

    # if all we need to do is always add the same methods to a set of classes
    # we might code them in a normal superclass and inherit in subclasses
    # metaclasses support much more dynamic behavior - configuration logic:

    print("\n> conditional extender")

    class ConditionalExtender(type):
        def __new__(meta,classname,supers,classdict):
            # only for testing purposes:
            some_test = lambda arg: True if arg else False
            arg1 = True
            eggsfunc1 = lambda obj: obj.value*3
            eggsfunc2 = lambda obj: obj.value*5

            other_test = lambda arg: True if arg else False
            arg2 = False
            hamfunc1 = lambda obj,arg: arg+'Ham'
            hamfunc2 = lambda obj,arg: arg+'HAM'
            # - - - - - - - - - - - - - - - - - - - - - - - 

            if some_test(arg1):
                classdict['eggs'] = eggsfunc1
            else:
                classdict['eggs'] = eggsfunc2
            
            if other_test(arg2):
                classdict['ham'] = hamfunc1
            else:
                classdict['ham'] = hamfunc2
            
            return type.__new__(meta,classname,supers,classdict)

    mc_dec_test(metaclass_type=ConditionalExtender)

def deco_augmentation():
    print("\nDECORATOR-BASED AUGMENTATION")
    # same as providing __init__ in a metaclass

    print("\n> basic extender")

    def DecoExtender(Class):
        Class.eggs = eggsfunc
        Class.ham = hamfunc
        return Class

    mc_dec_test(decorator_type=DecoExtender)
    
manual_augmentation()
meta_augmentation()
deco_augmentation()