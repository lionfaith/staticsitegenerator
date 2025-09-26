import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def standard_parent_node(self):
        return ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

    def test_init(self):
        node = self.standard_parent_node()
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)
        self.assertIsNotNone(node.children)
        self.assertIsInstance(node.children, list)
   
    def test_to_html(self):
        node = self.standard_parent_node()
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()