#!python
class ListInherited:
    """
    Use dir() to collect both instance attrs and names inherited from
    its classes; Python 3.X shows more names than 2.X because of the
    implied object superclass in the new-style class model; getattr()
    fetches inherited names not in self.__dict__; use __str__, not
    __repr__, or else this loops when printing bound methods!
    """
    def __attrnames(self):
        result=''
        for attr in dir(self):                              # instance dir()
            if attr[:2]=='__' and attr[-2:]=='__':          # skip internals
                result += f"\t{attr}\n"
            else:
                result += f"\t{attr}={getattr(self,attr)}\n"
        return result

    def __str__(self):
        return (f'<Instance of {self.__class__.__name__}, ' # my class name
                f'address {id(self)}:\n'                    # my address
                f'{self.__attrnames()}')                    # name=value list

if __name__ == '__main__':
    import testmixin as tm
    tm.tester(ListInherited)
