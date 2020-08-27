import unittest
import PorteFeuille

class TestPorteFeuille(unittest.TestCase):

    def test_init():
        pf = PorteFeuille(None, 3)
        self.assertEqual('foo'.upper(),'FOO')

    def test_upper(self):
        self.assertEqual('foo'.upper(),'FOO')

if __name__ == '__main__':
    unittest.main()
