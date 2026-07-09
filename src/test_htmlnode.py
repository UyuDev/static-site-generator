import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_none(self):
        node = HTMLNode()
        string1 = f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})"
        string2 = "HTMLNode(None, None, None, None)"
        self.assertEqual(string1, string2)

    def test_repr_text(self):
        node = HTMLNode(None, "Hello")
        string1 = f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})"
        string2 = "HTMLNode(None, Hello, None, None)"
        self.assertEqual(string1, string2)

    def test_repr_paragraph(self):
        node = HTMLNode("<p>", "Hello")
        string1 = f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})"
        string2 = "HTMLNode(<p>, Hello, None, None)"
        self.assertEqual(string1, string2)
    
    def test_repr_body(self):
        node = HTMLNode("<b>", None, ["<main>"])
        string1 = f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})"
        string2 = "HTMLNode(<b>, None, ['<main>'], None)"
        self.assertEqual(string1, string2)
    
    def test_props_to_html_paragraph(self):
        node = HTMLNode()
        node.props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
        string1 = node.props_to_html()
        string2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(string1, string2)