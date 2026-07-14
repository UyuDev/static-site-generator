from enum import Enum
from textnode import TextNode, text_node_to_html_node, code_to_html_node, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown: str) -> list[str]:
    split_text = markdown.split("\n\n")
    final_list = []
    for text in split_text:
        if text == "":
            continue
        final_list.append(text.strip())
    return final_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        i = 1
        while i < len(block) and block[i] == "#":
            i += 1
        if i >= 7 or len(block) == i:
            return BlockType.PARAGRAPH
        if i <= 6 and len(block) >= i+2:
            stripped_text = block[i:].strip()
            if block[i] == " " and stripped_text != "":
                return BlockType.HEADING
        return BlockType.PARAGRAPH
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_to_clean_text(block: str) -> str:
    return


def text_to_children(text: str) -> list[HTMLNode]:
    return


def block_type_to_html_node(tag: str, children: list[HTMLNode]) -> ParentNode:
    return


def blocks_to_children(blocks: list[str]) -> list[ParentNode]:
    return


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = blocks_to_children(blocks)
    node = ParentNode("div", children, None)
    return node
    