import unittest
from htmlnode import HTMLNode, LeafNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "url/of/image.jpg", "alt": "Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')

    def test_leaf_repr_none(self):
        node = LeafNode(None, None, None)
        string1 = f"LeafNode({node.tag}, {node.value}, {node.props})"
        self.assertEqual(string1, "LeafNode(None, None, None)")
    
    def test_leaf_repr_text(self):
        node = LeafNode(None, "Hello", None)
        string1 = f"LeafNode({node.tag}, {node.value}, {node.props})"
        self.assertEqual(string1, "LeafNode(None, Hello, None)")