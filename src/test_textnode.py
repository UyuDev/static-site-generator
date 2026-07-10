import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr_nourl(self):
        node = TextNode("sample text", TextType.TEXT)
        string1 = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        string2 = "TextNode(sample text, text, None)"
        self.assertEqual(string1, string2)

    def test_repr_image_url(self):
        node = TextNode("cool image", TextType.IMAGE, "image/goes/here")
        string1 = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        string2 = "TextNode(cool image, image, image/goes/here)"
        self.assertEqual(string1, string2)

    def test_repr_url(self):
        node = TextNode("Great chicken recipe", TextType.LINK, "https://alwaysfromscratch.com/cast-iron-chicken-breast/")
        string1 = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        string2 = "TextNode(Great chicken recipe, link, https://alwaysfromscratch.com/cast-iron-chicken-breast/)"
        self.assertEqual(string1, string2)

    def test_eq_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "example/url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {'href': 'example/url'})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'url/of/image.jpg', 'alt': 'This is an image node'})
        self.assertEqual(html_node.props['src'], "url/of/image.jpg")

    def test_incorrect_argument(self):
        node = "incorrect"
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_incorrect_type(self):
        node = TextNode("This is invalid", 55555, "invalid/url")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)








if __name__ == "__main__":
    unittest.main()