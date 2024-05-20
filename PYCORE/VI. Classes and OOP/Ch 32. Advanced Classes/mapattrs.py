#!python
"""
Main tool: mapattrs() maps all attributes on or inherited by an
instance to the instance or class from which they are inherited.

Assumes dir() gives all attributes of an instance. To simulate
inheritance, uses either the class's MRO tuple, which gives the
search order for new-syle classes (and all in 3.X), or a recursive
traversal to infer the DFLR order of classic classes in 2.X.

Also here: inheritance() gives version-neutral class ordering;
assorted dictionary tools using 3.X/2.7 comprehensions.
"""

import pprint

def trace(X,label='',end='\n'):
    print(label + pprint.pformat(X) + end)      # print nicely

def filterdictvals(D,V):
    """
    dict D with entries for value V removed.
    filterdictvals(dict(a=1,b=2,c=1),1) => {'b':2}
    """
    return {K: val for (K,val) in D.items() if val != V}

def invertdict(D):
    """
    dict D with values changed to keys (grouped by values).
    Values must all b ehashable to work as dict/set keys.
    invertdict(dict(a=1,b=2,c=1)) => {1: [a,c], 2: ['b']}
    """
    def keysof(V):
        return sorted(K for K in D.keys() if D[K]==V)

    return {V: keysof(V) for V in set(D.values())}

def dflr(cls):
    """
    Classic depth-first left-to-right order of class tree at cls.
    Cycles not possible: Python disallows on __bases__changes.
    """
    result = [cls]
    for super in cls.__bases__:
        result.append(dflr(super))
    return result

def inheritance(instance):
    """
    Inheritance order sequence: new-style (MRO) or classic (DFLR)
    """
    if hasattr(instance.__class__,'__mro__'):
        return (instance,) + instance.__class__.__mro__
    else:
        return [instance] + dflr(instance.__class__)

def mapattrs(instance, withobject=False, bysource=False):
    """
    dict with keys giving all inherited attributes of instance,
    with values giving the object that each is inherited from.
    withobject: False = remove 'object' built-in class attributes.
    by source: True = group result by objects instead of attributes.
    Supports classes with slots that preclude __dict__ in instances.
    """
    attr2obj = {}
    inherits = inheritance(instance)

    for attr in dir(instance):
        for obj in inherits:
            if hasattr(obj,'__dict__') and attr in obj.__dict__:
                attr2obj[attr] = obj
                break
    
    if not withobject:
        attr2obj = filterdictvals(attr2obj,object)
    
    return attr2obj if not bysource else invertdict(attr2obj)


if __name__ == '__main__':
    print("\nSELF - TEST")

    class A:            attr1 = 'A'
    class B(A):         attr2 = 'B'
    class C(A):         attr1 = 'C'
    class D(B,C):       pass

    def basic():

        L=[1,2,1,2,1]
        D=dict(a=1,b=2,c=1,d=2,e=1)

        print("\n> trace:")
        trace(L,'test list ',end='')
        trace(D,'test dict ',end='')

        print("\n> filter dict values:")
        print('1:',filterdictvals(D,1))
        print('2:',filterdictvals(D,2))

        print("\n> invert dict:")
        print(invertdict(D))

        print("\n> DFLR:")
        print(dflr(D))
    
        print("\n> inheritance:")
        for x in inheritance(I): print(x)

    def simple():
        I = D()
        print(f"Py => {I.attr1}\n")                 # Python search == ours ?
        trace(inheritance(I),           'INH\n')    # inheritance order
        trace(mapattrs(I),              'ATTRS\n')  # attrs => source
        trace(mapattrs(I,bysource=True),'OBJS\n')   # source => attrs
    
    def real():
        import tkinter as tk
        I = tk.Button()
        trace(mapattrs(I,bysource=True),'OBJS\n')   # source => attrs

    class A:            __slots__ = ['a','b']; x=1; y=2
    class B(A):         __slots__ = ['b','c']
    class C(A):         x=2
    class D(B,C):
        z=3
        def __init__(self):
            self.name = 'Bob'

    def slots():
        I = D()
        trace(mapattrs(I,bysource=True))

    slots()
