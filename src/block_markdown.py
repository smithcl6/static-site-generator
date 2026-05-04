from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    result = []
    for block in blocks:
        if block != "":
            result.append(block)
    return result

def block_to_block_type(block:str)->BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")

    if block.startswith(">"):
        for line in lines:
            if line.startswith(">") and len(line) > 1:
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if line.startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        for i in range(0, len(lines)):
            if lines[i].startswith(f"{i+1}. "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown:str)->ParentNode:

    def text_to_children(text:str)->list[LeafNode]:
        text_nodes = text_to_textnodes(text)
        children:list[LeafNode] = []
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            children.append(html_node)
        return children
    
    def paragraph_to_html(block:str)->ParentNode:
        lines = block.split("\n")
        paragraph = " ".join(lines)
        children = text_to_children(paragraph)
        return ParentNode("p", children)
    
    def heading_to_html(block:str)->ParentNode:
        header_level = 0
        for char in block:
            if char == "#":
                header_level += 1
            else:
                break
        text = block[header_level + 1 :]
        children = text_to_children(text)
        return ParentNode(f"h{header_level}", children)

    def code_to_html(block:str)->ParentNode:
        text = block[4:-3]
        raw_text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])

    def quote_to_html(block:str)->ParentNode:
        lines = block.split("\n")
        new_lines:list[str] = []
        for line in lines:
            new_lines.append(line.lstrip(">").strip())
        text = " ".join(new_lines)
        children = text_to_children(text)
        return ParentNode("blockquote", children)

    def unordered_list_to_html(block:str)->ParentNode:
        items = block.split("\n")
        html_items:list[ParentNode] = []
        for item in items:
            text = item[2:]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)

    def ordered_list_to_html(block:str)->ParentNode:
        items = block.split("\n")
        html_items:list[ParentNode] = []
        for item in items:
            section = item.split(". ", 1)
            text = section[1]
            children = text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ol", html_items)

    def block_to_html(block:str)->LeafNode:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                return paragraph_to_html(block)
            case BlockType.HEADING:
                return heading_to_html(block)
            case BlockType.CODE:
                return code_to_html(block)
            case BlockType.QUOTE:
                return quote_to_html(block)
            case BlockType.UNORDERED_LIST:
                return unordered_list_to_html(block)
            case BlockType.ORDERED_LIST:
                return ordered_list_to_html(block)
            case _:
                raise ValueError("invalid block type")

    blocks:list[str] = markdown_to_blocks(markdown)
    children:list[LeafNode] = []
    for block in blocks:
        children.append(block_to_html(block))
    return ParentNode("div", children, None)
