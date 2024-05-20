#!python
"""
reloadall.py: transitively reload nested modules (2.X + 3.X).
Call reload_all with one or more imported module objects.
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
    
def transitive_reload(module,visited):
    # trap cycles, duplicates
    if not module in visited:
        status(module)
        # reload this module
        try_reload(module)
        visited[module]=True

        # and visit children
        for attr in module.__dict__.values():
            # for all attributes
            if type(attr) == types.ModuleType:
                # recur if module type
                transitive_reload(attr,visited)

def reload_all(*args):
    # main entry point
    visited = {}

    # for all passed in
    for arg in args:
        if type(arg) == types.ModuleType:
            transitive_reload(arg,visited)

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
    tester(reload_all,'reloadall')