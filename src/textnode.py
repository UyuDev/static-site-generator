from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # redefines ==
    def __eq__(self, other: TextType) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    # redefines the string representation, replacing the memory-address format
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            node = LeafNode(None, text_node.text)
            return node
        case TextType.BOLD:
            node = LeafNode("b", text_node.text)
            return node
        case TextType.ITALIC:
            node = LeafNode("i", text_node.text)
            return node 
        case TextType.CODE:
            node = LeafNode("code", text_node.text)
            return node 
        case TextType.LINK:
            node = LeafNode("a", text_node.text, {"href": text_node.url})
            return node 
        case TextType.IMAGE:
            node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return node 
        case _:
            raise Exception("invalid node type")