import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_2 = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_single_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_2 = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_single_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes_2 = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_delimiter_at_start(self):
        node = TextNode("`code block` example", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_2 = [
        TextNode("code block", TextType.CODE),
        TextNode(" example", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_multiple_same_delimiter(self):
        node = TextNode("`code block` 123 `code block``code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_2 = [
        TextNode("code block", TextType.CODE),
        TextNode(" 123 ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_no_delimiter(self):
        node = TextNode("no delimiter just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_2 = [TextNode("no delimiter just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, new_nodes_2)
    
    def test_non_text_node(self):
        node = TextNode("`code block` 123 `code block``code block`", TextType.TEXT)
        node_2 = TextNode("This is a link node", TextType.LINK, "example/url")
        new_nodes = split_nodes_delimiter([node, node_2], "`", TextType.CODE)
        new_nodes_2 = [
        TextNode("code block", TextType.CODE),
        TextNode(" 123 ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode("code block", TextType.CODE),
        TextNode("This is a link node", TextType.LINK, "example/url"),
        ]
        self.assertEqual(new_nodes, new_nodes_2)

    def test_invalid_delimiter(self):
        node = TextNode("`code block` example", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "", TextType.CODE)
    
    def test_odd_delimiter(self):
        node = TextNode("`code block`code block`", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)