import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(f"{node}", f"HTMLNode(tag=None,value=None,children=None, props=None)")
    
    def test_props_to_html(self):
        tag = "Test"
        value = "Hello world!"
        children = None
        props = { "href": "https://www.google.com", "target": "_blank" }
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()