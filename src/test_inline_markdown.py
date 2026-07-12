import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches
        )
    
class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches
        )
    
    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links(
            "This is text with a link [to wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page) and [the definition of link](https://en.wiktionary.org/wiki/link)"
        )
        self.assertListEqual(
            [("to wiktionary", "https://en.wiktionary.org/wiki/Wiktionary:Main_Page"), ("the definition of link", "https://en.wiktionary.org/wiki/link")], matches
        )

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_only_text(self):
        node = TextNode("This is some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is some text", TextType.TEXT)], new_nodes)

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) image example",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image example", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_duplicates(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_mixed(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_only_text(self):
        node = TextNode("This is some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is some text", TextType.TEXT)], new_nodes)
    
    def test_split_links_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_split_links_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) link example",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" link example", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_duplicates(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to boot dev", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_mixed(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )