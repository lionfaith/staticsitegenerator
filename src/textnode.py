from enum import Enum
import re

class TextType(Enum):
    TEXT = "text(plain)"
    BOLD = "**bold**"
    ITALIC = "_italic_"
    CODE = "`code`"
    LINK = "[anchor text](url)"
    IMG = "![alt text](url)"

MARKDOWN_IMAGES_RE = r"\!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINKS_RE = r"\[(.*?)\]\((.*?)\)"

class TextNode:
    def __init__(self,text: str,text_type:TextType,url=None):
        """text: The text content of the node
        text_type: The type of text this node contains,
            which is a member of the TextType enum.
        url: The URL of the link or image, if the text is a link.
            Default to None if nothing is passed in."""
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    result = []
    for c in old_nodes:
        if c.text_type is not TextType.TEXT:
            result.append(c)
            continue
        split = c.text.partition(delimiter)
        if split[0] != "":
            result.append(TextNode(split[0],TextType.TEXT))
        while not split[1] == "":
            split = split[2].partition(delimiter)
            result.append(TextNode(split[0], text_type))
            if split[1] == "":
                result.append(TextNode(f"(!!{delimiter}!!)",TextType.TEXT))
                break
            split = split[2].partition(delimiter)
            result.append(TextNode(split[0],TextType.TEXT))
    return result

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    return split_nodes_imglike(old_nodes, TextType.IMG, MARKDOWN_IMAGES_RE)

def split_nodes_link(old_nodes: list[TextNode]):
    return split_nodes_imglike(old_nodes, TextType.LINK, MARKDOWN_LINKS_RE)

def split_nodes_imglike(old_nodes: list[TextNode], tt: TextType, RExpr):
    result = []
    for c in old_nodes:
        if c.text_type is not TextType.TEXT:
            result.append(c)
            continue
        t = c.text
        while t:
            m = re.search(RExpr,t)
            if m is None:
                result.append(TextNode(t, TextType.TEXT))
                break
            if m.start(0) > 0:
                result.append(TextNode(t[:m.start(0)], TextType.TEXT))
            result.append(TextNode(m.group(1), tt, m.group(2)))
            t = t[m.end(0):]
    return result
        
def text_to_textnodes(text):
    result = [TextNode(text, TextType.TEXT)]
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

MARKDOWN_HEAD_RE = r"#{1,6} (.*)"  # removed \n
MARKDOWN_CODE_RE = r"```(?:\n)?([\s\S]*?(?:\n)?)```"
MARKDOWN_QUOTE_LINE_RE = r"> (.*)"  # removed \n
MARKDOWN_ULIST_LINE_RE = r"- (.*)"  # removed \n
MARKDOWN_OLIST_LINE_RE = r"([1-9][0-9]*)\. (.*)"  # removed \n

def markdown_to_blocks(markdown: str) -> list[str]:
    return [s.strip() for s in markdown.split("\n\n") if s!=""]

def block_to_block_type(markdownblock: str):
    if re.match(MARKDOWN_HEAD_RE, markdownblock):
        return BlockType.HEAD
    if re.match(MARKDOWN_CODE_RE, markdownblock):
        return BlockType.CODE
    lines = markdownblock.split("\n")
    if lines[0].lstrip().startswith(">"):
        quote = True
        for l in lines[1:]:
            if not l.lstrip().startswith(">"):
                quote = False
                break
        if quote:
            return BlockType.QUOTE
    if re.match(MARKDOWN_ULIST_LINE_RE, lines[0]):
        ulist = True
        for l in lines[1:]:
            if not re.match(MARKDOWN_ULIST_LINE_RE, l):
                ulist = False
                break
        if ulist:
            return BlockType.ULIST
    m = re.match(MARKDOWN_OLIST_LINE_RE, lines[0])
    if m is not None and m.group(1) == "1":
        olist = True
        i=2
        for l in lines[1:]:
            m = re.match(MARKDOWN_OLIST_LINE_RE, l)
            if m is None or m.group(1) != f"{i}":
                olist = False
                break
            i += 1
        if olist:
            return BlockType.OLIST
    return BlockType.PARA

def extract_heading_from_block(textblock: str) -> str:
    m = re.match(MARKDOWN_HEAD_RE, textblock)
    if m is not None:
        return m.group(1)
    else:
        raise Exception(f"I won't extract a heading out of a non HEAD block. It means MARKDOWN_HEAD_RE didn't matched.")

def extract_code_from_block(textblock: str) -> str:
    m = re.match(MARKDOWN_CODE_RE, textblock, re.DOTALL)
    if m is not None:
        return m.group(1)
    else:
        raise Exception(f"I won't extract code out of a non CODE block. It means MARKDOWN_CODE_RE didn't matched.")

def extract_quote_from_block(textblock: str) -> str:
    # Remove the first '>' and optional space from each line
    return "\n".join([l[2:] if l.startswith("> ") else l for l in textblock.split("\n")])

def extract_items_from_ulist_block(textblock: str) -> list[str]:
    return [
        m.group(1)
        for l in textblock.split("\n")
        if (m := re.match(MARKDOWN_ULIST_LINE_RE, l))
    ]

def extract_items_from_olist_block(textblock: str) -> list[str]:
    return [
        m.group(2)
        for l in textblock.split("\n")
        if (m := re.match(MARKDOWN_OLIST_LINE_RE, l))
    ]

