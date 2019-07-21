print('hello.py init')

__all__=['A','__C','Cat']

A=[1,2,3]
_B=['a','b','c']
__C=('Hello','Tom')

def say():
    print('say hello again')

class Cat:
    def eat(self):
        print('Cat is eating...')

if __name__ == '__main__':
    # do test:
    print('A=%s,_B=%s,__C=%s' % (A,_B,__C))
    say()
    c=Cat()
    c.eat()