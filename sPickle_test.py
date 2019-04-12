import unittest
import sPickle
import os
import datetime

class TestSPickle(unittest.TestCase):
    def setUp(self):
        self.testfn='sPickle.testfile'

    def tearDown(self):
        if os.path.exists(self.testfn):
            os.remove(self.testfn)

    def test_empty(self):
        with open(self.testfn, 'wb') as f:
            sPickle.s_dump([], f)
        with open(self.testfn, 'rb') as f:
            for elt in sPickle.s_load(f):
                self.fail('found element for stream that should be empty: ' + str(elt))

    def _assertArray(self, expected, actual):
         self.assertEqual(len(expected), len(actual))
         for i in range(len(expected)):
             self.assertEqual(expected[i], actual[i])

    def _assertArrayFloats(self, expected, actual, delta):
         self.assertEqual(len(expected), len(actual))
         for i in range(len(expected)):
             self.assertEqual(expected[i], actual[i], delta)


    def _dump(self, iterable):
        with open(self.testfn, 'wb') as f:
            sPickle.s_dump(iterable, f)

    def _load(self):
        with open(self.testfn, 'rb') as f:
            return list(sPickle.s_load(f))

    def test_ints(self):
        ints = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        self._dump(ints)
        self._assertArray(ints, self._load())
        
    def test_floats(self):
        floats = [-3.0, -2.5, -1.0, 0.0, 1.0, 2.5, 3.0]
        self._dump(floats)
        self._assertArrayFloats(floats, self._load(), .001)

    def test_strings(self):
        strings=['a', 'bCD', 'EF', 'G']
        self._dump(strings)
        self._assertArray(strings, self._load())

    def test_stringsWithNewlines(self):
        strings=['\n', 'a\n', 'b\nCD', '\nEF', '\nG\n']
        self._dump(strings)
        self._assertArray(strings, self._load())

    def test_dict(self):
        d = {'int_field': 1, 
             'float_field': 2.3, 
             'string_field': 'hello', 
             'date_field': datetime.datetime(2015, 1, 16, 19, 44, 0)}
        self._dump([d])
        self._assertArray([d], self._load())

    def test_writeByteArrayStream(self):
        with open(self.testfn, 'wb') as f:
            sPickle.writeByteArrayStream([b'abc\\\n'], f)
        with open(self.testfn, 'rb') as f:
            b = f.read()
        self.assertEqual(b'abc\\\\\\\n\n', b)

    def test_readByteArrayStream(self):
        with open(self.testfn, 'wb') as f:
            f.write(b'abc\\\\\\\n\n')
        with open(self.testfn, 'rb') as f:
            lst = list(sPickle.readByteArrayStream(f))
            self._assertArray([b'abc\\\n'], lst)

    def test_readByteArrayStream_empty(self):
        with open(self.testfn, 'wb') as f:
            pass
        with open(self.testfn, 'rb') as f:
            lst = list(sPickle.readByteArrayStream(f))
            self._assertArray([], lst)

    def test_readByteArrayStream_oneElement(self):
        with open(self.testfn, 'wb') as f:
            f.write(b'a\n')
        with open(self.testfn, 'rb') as f:
            lst = list(sPickle.readByteArrayStream(f))
            self._assertArray([b'a'], lst)



if __name__ == '__main__':
    unittest.main()
