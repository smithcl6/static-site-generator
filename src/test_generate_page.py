import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Header"), "Header")
        self.assertNotEqual(extract_title("# Header "), "Header ")
        self.assertEqual(extract_title("# Header   "), "Header")
        self.assertEqual(extract_title("# Header   and 3 extra spaces."), "Header   and 3 extra spaces.")
        
