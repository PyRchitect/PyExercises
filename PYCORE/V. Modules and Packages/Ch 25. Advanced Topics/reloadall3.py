#!python
"""
reloadall3.py: transitively reload nested modules (explicit stack)
"""

import types
from importlib import reload

def status(module):
    print(f"Reloading module: {module.__name__}")

def try_reload(module):
    try:
        reload(module)
    except:
        print(f"FAILED: {module}")
    
def transitive_reload(modules,visited):
    while modules:
        next = modules.pop()
        status(next)
        try_reload(next)
        visited.add(next)

        modules.extend(x for x in next.__dict__.values()
                       if type(x) == types.ModuleType and x not in visited)        

def reload_all(*modules):
    transitive_reload(list(modules),set())

def tester(reloader, modname):
    # self-test code

    # import on tests only:
    import sys
    from importlib import import_module

    # command line (or passed):
    if len(sys.argv) > 1: modname = sys.argv[1]

    # import by name string:
    module = import_module(modname)
    reloader(module)

if __name__ == '__main__':
    # test: reload myself
    tester(reload_all,'reloadall3')