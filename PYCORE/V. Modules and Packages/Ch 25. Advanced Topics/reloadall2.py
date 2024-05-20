#!python
"""
reloadall2.py: transitively reload nested modules (alternative coding)
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
    
def transitive_reload(objects,visited):
    for obj in objects:
        if type(obj) == types.ModuleType and obj not in visited:
            status(obj)
            try_reload(obj)
            visited.add(obj)
            transitive_reload(obj.__dict__.values(),visited)

def reload_all(*args):
    transitive_reload(args,set())

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
    tester(reload_all,'reloadall2')