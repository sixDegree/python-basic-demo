'''
>>> hello([4,5,6])
hello: [4,5,6]
'''
def hello(x):
    '''
    doc test demo -- helo

    >>> hello('Tom')
    hello: Tom
    >>> hello(1/0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero
    >>> hello([1,2,3])
    hello: [1,2,3]
    '''
    print('hello:',x)


if __name__=='__main__':
    import doctest
    doctest.testmod()