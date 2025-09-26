import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("Test", TextType.ITALIC)
        self.assertEqual(f"{node}", f"TextNode(Test, _italic_, None)")
    
    def test_init(self):
        a = "Test"
        t = TextType.ITALIC
        node = TextNode(a, t)
        self.assertEqual(node.text, a)
        self.assertEqual(node.text_type, t)
    
    def test_init_with_url(self):
        a = "Test"
        t = TextType.ITALIC
        u = "http://boot.dev"
        node = TextNode(a, t, u)
        self.assertEqual(node.text, a)
        self.assertEqual(node.text_type, t)
        self.assertEqual(node.url, u)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes,test_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [url](https://random.rn/yo) and another [url2](https://galazy.next/ET)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("url", TextType.LINK, "https://random.rn/yo"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "url2", TextType.LINK, "https://galazy.next/ET"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev"),
                        ])
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEAD)

    def test_block_to_block_type_code(self):
        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        quote_block = "> This is a quote\n> still a quote"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        ulist_block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ulist_block), BlockType.ULIST)

    def test_block_to_block_type_ordered_list(self):
        olist_block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(olist_block), BlockType.OLIST)

    def test_block_to_block_type_paragraph(self):
        para_block = "This is a normal paragraph.\nIt has multiple lines."
        self.assertEqual(block_to_block_type(para_block), BlockType.PARA)


if __name__ == "__main__":
    unittest.main()