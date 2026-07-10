import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_4_levels_deep(self):
        great_grandchild_node = LeafNode("i", "great-grandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><i>great-grandchild</i></b></span></div>",
        )
    
    def test_to_html_4_levels_deep_list(self):
        great_grandchild_node = LeafNode("li", "First item")
        great_grandchild_node2 = LeafNode("li", "Second item")
        great_grandchild_node3 = LeafNode("li", "Third item")
        grandchild_node = ParentNode("ul", [great_grandchild_node, great_grandchild_node2, great_grandchild_node3])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></span></div>",
        )

    def test_to_html_5_levels_deep(self):
        gg_grandchild_node = LeafNode("u", "deep")
        great_grandchild_node = ParentNode("i", [gg_grandchild_node])
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><i><u>deep</u></i></b></span></div>",
        )
    
    def test_to_html_5_2_levels_deep(self):
        gg_grandchild_node = LeafNode("u", "first")
        gg_grandchild_node2 = LeafNode("u", "second")
        great_grandchild_node = ParentNode("i", [gg_grandchild_node, gg_grandchild_node2])
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><i><u>first</u><u>second</u></i></b></span></div>",
        )
    
    def test_to_html_5_3_levels_deep(self):
        gg_grandchild_node = LeafNode("i", "first")
        gg_grandchild_node2 = LeafNode(None, "second")
        gg_grandchild_node3 = LeafNode("i", "third")
        great_grandchild_node = ParentNode("u", [gg_grandchild_node, gg_grandchild_node2, gg_grandchild_node3])
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><u><i>first</i>second<i>third</i></u></b></span></div>",
        )