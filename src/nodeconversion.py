from htmlnode import *
from textnode import *

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img","",{"src": text_node.url, "alt": text_node.text})

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_blocks = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", html_blocks)

def block_to_html_node(block: str) -> ParentNode | LeafNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEAD:
            level = block.count("#", 0, block.find(" "))
            content = extract_heading_from_block(block)
            nodes = [text_node_to_html_node(tn) for tn in text_to_textnodes(content)]
            return ParentNode(f"h{level}", nodes)
        case BlockType.CODE:
            code = extract_code_from_block(block)
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, code)])])
        case BlockType.QUOTE:
            quote = extract_quote_from_block(block)
            nodes = [text_node_to_html_node(tn) for tn in text_to_textnodes(quote)]
            return ParentNode("blockquote", nodes)
        case BlockType.ULIST:
            items = extract_items_from_ulist_block(block)
            li_nodes = [
                ParentNode("li", [text_node_to_html_node(tn) for tn in text_to_textnodes(item)])
                for item in items
            ]
            return ParentNode("ul", li_nodes)
        case BlockType.OLIST:
            items = extract_items_from_olist_block(block)
            li_nodes = [
                ParentNode("li", [text_node_to_html_node(tn) for tn in text_to_textnodes(item)])
                for item in items
            ]
            return ParentNode("ol", li_nodes)
        case BlockType.PARA:
            para = block.replace("\n", " ")
            nodes = [text_node_to_html_node(tn) for tn in text_to_textnodes(para)]
            return ParentNode("p", nodes)