import unittest
import os
from ezdir import up, find

class TestChanger(unittest.TestCase):
    def test_up(self):
        start = os.getcwd()
        up(1)
        self.assertNotEqual(os.getcwd(), start)
        os.chdir(start)

    def test_find_not_found(self):
        with self.assertRaises(FileNotFoundError):
            find("folder_that_does_not_exist")

if __name__ == "__main__":
    unittest.main()