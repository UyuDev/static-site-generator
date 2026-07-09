import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_repr_nourl(self):
        node = TextNode("sample text", TextType.PLAIN_TEXT)
        string1 = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        string2 = "TextNode(sample text, plain text, None)"
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
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()