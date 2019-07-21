import unittest

class MyTest(unittest.TestCase):
    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')

    def test_dict(self):
        print('test 1')
        d={'a':1,'b':2}
        self.assertEqual(d['a'],1)
        self.assertEqual(d['b'],2)
        self.assertTrue(isinstance(d, dict))

    def testdict2(self):
        print('test 2')
        d={'a':1,'b':2}
        with self.assertRaises(KeyError):   # 期待抛出指定类型的Error
            value = d['c']

if __name__ == '__main__':
    unittest.main()