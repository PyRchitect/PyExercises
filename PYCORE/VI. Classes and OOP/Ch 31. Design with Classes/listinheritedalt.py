#!python
class ListInheritedAlt:
    """
    Use dir() to collect both instance attrs and names inherited from
    its classes; Python 3.X shows more names than 2.X because of the
    implied object superclass in the new-style class model; getattr()
    fetches inherited names not in self.__dict__; use __str__, not
    __repr__, or else this loops when printing bound methods!
    """
    def __attrnames(self,indent=' '*4):
        max_width = 60
        unders = []        
        result = (f"Unders{'-'*max_width}\n"
                  f"{indent}"
                  "%s\n"                       # unders filled in at the end
                  f"Others{'-'*max_width}\n")
        for attr in dir(self):
            if attr[:2]=='__' and attr[-2:]=='__':          # skip internals
                unders.append(attr)
            else:
                display = str(getattr(self,attr))                
                if (len(attr)+len(indent)+len(' = ')+len(display))>max_width:
                    width = max_width-len(attr)-len(indent)
                    start = int(width/2)
                    end = width-start
                    display = display[:start]+'...'+display[-end:]

                result += f"{indent}{attr} = {display}\n"
        return result % ', '.join(unders)

    def __str__(self):
        return (f'<Instance of {self.__class__.__name__}, ' # my class name
                f'address {id(self)}:\n'                    # my address
                f'{self.__attrnames()}')                    # name=value list

if __name__ == '__main__':
    import testmixin as tm
    tm.tester(ListInheritedAlt)
