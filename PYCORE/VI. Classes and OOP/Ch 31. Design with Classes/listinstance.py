#!python

class ListInstance:
    """
    Mix-in class that provides a formatted print() or str() of instances via
    inheritance of __str__ coded here; displays instance attrs only; self is
    instance of lowest class; __X names avoid clashing with client's attrs
    """
    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):
            result += f'\t{attr}={self.__dict__[attr]}\n'
        return result
    
    def __str__(self):
        return (f'<Instance of {self.__class__.__name__}, ' # my class name
                f'address {id(self)}:\n'                    # my address
                f'{self.__attrnames()}')                    # name=value list

if __name__ == '__main__':
    import testmixin as tm
    tm.tester(ListInstance)
