import unittest

from funcy import Fn

class TestObj:
    def __init__(self):
        self.foo = 'foo'
        self.boo = 10
    @property
    def thing(self):
        return self

class FuncyTest(unittest.TestCase):
    def test(self):
        testobj = TestObj()
        myvar = Fn(1., name = 'myvar')
        myvar += 1
        self.assertEqual(myvar, 2)
        myget = Fn(testobj).get('thing', 'foo').get[2] * 3
        self.assertEqual(myget, 'ooo')
        holdvar = myget >> Fn(str)
        self.assertEqual(holdvar, myget)
        myfn = Fn(name = 'var1') * Fn()
        self.assertEqual(myfn(4, var1 = 3), myfn(3, 4), 12)
        myget = Fn(testobj).get('thing', 'thing', 'boo')
        myfn = Fn(myget, 2).op(pow)
        self.assertEqual(myfn, 100)
        myvar = myfn >> [float]
        vals = myvar.value, myvar.value, myvar.value
        vals = [list(v) for v in vals]
        self.assertEqual(vals, [[100.], [100., 100.], [100., 100., 100.]])
        self.assertEqual(len(myvar), 3)

if __name__ == '__main__':
    unittest.main()
