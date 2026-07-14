import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, blocks_to_children, text_to_children, block_to_clean_text, block_to_heading, code_to_html_node
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excessive_newlines_2(self):
        md = """
This is **bolded** paragraph
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excessive_whitespace(self):
        md = """
          This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items          
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_single_block(self):
        md = """
          This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items          
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_only_whitespace(self):
        md = "                            "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [''])
    
class TestMarkdownBlocks(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "sdfhsfhdsffhsdffhsdfhsd"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_headings_1(self):
        block = "# Daily Journal"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_headings_2(self):
        block = "## July"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_headings_3(self):
        block = "### July 12 2026"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_headings_4(self):
        block = "#### heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_headings_5(self):
        block = "##### heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_headings_6(self):
        block = "###### heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        block = "```\nprint('hello world')\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = ">quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_2(self):
        block = "> quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- item one"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_unordered_list_2(self):
        block = "- item one\n- item two\n- item three"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. item one"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_ordered_list_2(self):
        block = "1. item one\n2. item two\n3. item three"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


class TestTextToChildren(unittest.TestCase):
    def test_text_to_children(self):
        new_nodes = text_to_children("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        # copied from test_text_to_textnodes and used as a reference
        text_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        target = [
            LeafNode(None, "This is "),
            LeafNode("b", "text"),
            LeafNode(None, " with an "),
            LeafNode("i", "italic"),
            LeafNode(None, " word and a "),
            LeafNode("code", "code block"),
            LeafNode(None, " and an "),
            LeafNode("img", "", {'src': 'https://i.imgur.com/fJRm4Vk.jpeg', 'alt': 'obi wan image'}),
            LeafNode(None, " and a "),
            LeafNode("a", "link", {'href': 'https://boot.dev'}),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)
    
    def test_text_to_children_only_text(self):
        new_nodes = text_to_children("sample text")
        text_nodes = [TextNode("sample text", TextType.TEXT)]
        target = [LeafNode(None, "sample text")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)
    
    def test_text_to_children_only_bold(self):
        new_nodes = text_to_children("**sample text**")
        text_nodes = [TextNode("sample text", TextType.BOLD)]
        target = [LeafNode("b", "sample text")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_only_italic(self):
        new_nodes = text_to_children("_sample text_")
        text_nodes = [TextNode("sample text", TextType.ITALIC)]
        target = [LeafNode("i", "sample text")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_only_code(self):
        new_nodes = text_to_children("`sample text`")
        text_nodes = [TextNode("sample text", TextType.CODE)]
        target = [LeafNode("code", "sample text")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_only_image(self):
        new_nodes = text_to_children("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        text_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        target = [LeafNode(None, "This is text with an "), LeafNode("img", "", {'src': 'https://i.imgur.com/zjjcJKZ.png', 'alt': 'image'})]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_only_link(self):
        new_nodes = text_to_children("This is text with a link [to boot dev](https://www.boot.dev)")
        text_nodes = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ]
        target = [LeafNode(None, "This is text with a link "), LeafNode("a", "to boot dev", {'href': 'https://www.boot.dev'})]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_invalid_syntax_image(self):
        new_nodes = text_to_children("This is text with an image](https://i.imgur.com/zjjcJKZ.png)")
        text_nodes = [TextNode("This is text with an image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)]
        target = [LeafNode(None, "This is text with an image](https://i.imgur.com/zjjcJKZ.png)")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

    def test_text_to_children_invalid_syntax_link(self):
        new_nodes = text_to_children("This is text with a link [to boot dev)(https://www.boot.dev)")
        text_nodes = [TextNode("This is text with a link [to boot dev)(https://www.boot.dev)", TextType.TEXT)]
        target = [LeafNode(None, "This is text with a link [to boot dev)(https://www.boot.dev)")]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].tag, target[i].tag)
            self.assertEqual(new_nodes[i].value, target[i].value)
            self.assertEqual(new_nodes[i].props, target[i].props)

class TestCodeToHtmlNode(unittest.TestCase):
    def test_code_to_html_node(self):
        block = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        parent_node = code_to_html_node(block)
        target = ParentNode("pre", [LeafNode("code", "This is text that _should_ remain\nthe **same** even with inline stuff\n")])
        parent_child = parent_node.children[0]
        target_child = target.children[0]
        self.assertEqual(parent_node.tag, target.tag)
        self.assertEqual(parent_child.tag, target_child.tag)
        self.assertEqual(parent_child.value, target_child.value)
    
    def test_code_to_html_node_2(self):
        block = """
```python
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        parent_node = code_to_html_node(block)
        target = ParentNode("pre", [LeafNode("code", "This is text that _should_ remain\nthe **same** even with inline stuff\n")])
        parent_child = parent_node.children[0]
        target_child = target.children[0]
        self.assertEqual(parent_node.tag, target.tag)
        self.assertEqual(parent_child.tag, target_child.tag)
        self.assertEqual(parent_child.value, target_child.value)
    
    def test_code_to_html_node_3(self):
        block = """
```bash
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        parent_node = code_to_html_node(block)
        target = ParentNode("pre", [LeafNode("code", "This is text that _should_ remain\nthe **same** even with inline stuff\n")])
        parent_child = parent_node.children[0]
        target_child = target.children[0]
        self.assertEqual(parent_node.tag, target.tag)
        self.assertEqual(parent_child.tag, target_child.tag)
        self.assertEqual(parent_child.value, target_child.value)