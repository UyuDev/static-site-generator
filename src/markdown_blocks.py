from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
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

def code_to_html_node(block: str) -> LeafNode:
    return

def block_to_heading(block: str) -> str:
    return

def block_to_html_node(tag: str, children: list[HTMLNode]) -> HTMLNode:
    return


def block_to_clean_text(block: str) -> str:
    return


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    final_list = []
    for node in text_nodes:
        leaf_node = text_node_to_html_node(node)
        final_list.append(leaf_node)
    return final_list

def blocks_to_children(blocks: list[str]) -> list[ParentNode]:
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.UNORDERED_LIST:
            split_lines = block.split("\n")
            list_children = []
            for line in split_lines:
                new_text = block_to_clean_text(line)
                children = text_to_children(new_text)
                new_node = block_to_html_node("li", children)
                list_children.append(new_node)
            unordered_list_node = block_to_html_node("ul", list_children)
            parent_nodes.append(unordered_list_node)
        elif block_type == BlockType.ORDERED_LIST:
            split_lines = block.split("\n")
            list_children = []
            for line in split_lines:
                new_text = block_to_clean_text(line)
                children = text_to_children(new_text)
                new_node = block_to_html_node("li", children)
                list_children.append(new_node)
            ordered_list_node = block_to_html_node("ol", list_children)
            parent_nodes.append(ordered_list_node)
        elif block_type == BlockType.CODE:
            code_node = code_to_html_node(block)
            parent_nodes.append(code_node)
        else:
            new_text = block_to_clean_text(block)
            children = text_to_children(new_text)
            if block_type == BlockType.QUOTE:
                new_node = block_to_html_node("blockquote", children)
                parent_nodes.append(new_node)
            elif block_type == BlockType.HEADING:
                tag = block_to_heading(block)
                new_node = block_to_html_node(tag, children)
                parent_nodes.append(new_node)
            elif block_type == BlockType.PARAGRAPH:
                new_node = block_to_html_node("p", children)
                parent_nodes.append(new_node)
    return parent_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = blocks_to_children(blocks)
    node = ParentNode("div", children, None)
    return node
    