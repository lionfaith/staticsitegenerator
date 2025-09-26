import unittest
import generate

class Testextract_title(unittest.TestCase):
    def test_simple(self):
        txt = "# Hello"
        self.assertEqual("Hello", generate.extract_title(txt))
    
    def test_no_title(self):
        txt = "Blah blah blah\nBuluh Buluh Buluh\nTim tagada tzoingtzoing tsimboum tralala"
        self.assertRaises(Exception, generate.extract_title, txt)