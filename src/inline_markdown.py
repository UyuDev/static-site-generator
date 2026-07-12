from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    valid_delimiter = ["**", "_", "`"]
    if delimiter not in valid_delimiter:
        raise Exception("invalid Markdown delimiter")
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid Markdown syntax - missing closing delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                elif i % 2 == 0:
                    new_node = TextNode(split_text[i], TextType.TEXT)
                    final_list.append(new_node)
                else:
                    new_node = TextNode(split_text[i], text_type)
                    final_list.append(new_node)
    return final_list
# tuple should contain alt text and URL of MD images
def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
# tuple should contain anchor text and URL link
def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            remaining_text = node.text
            matches = extract_markdown_images(node.text)
            for alt_text, url in matches:               
                section = f"![{alt_text}]({url})"
                split_text = remaining_text.split(section, maxsplit=1)
                if split_text[0] != "":
                    new_node = TextNode(split_text[0], TextType.TEXT)
                    final_list.append(new_node)
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                final_list.append(image_node)
                remaining_text = split_text[1]
            if remaining_text != "":
                new_node = TextNode(remaining_text, TextType.TEXT)
                final_list.append(new_node)
    return final_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            remaining_text = node.text
            matches = extract_markdown_links(node.text)
            for anchor_text, url in matches:               
                section = f"[{anchor_text}]({url})"
                split_text = remaining_text.split(section, maxsplit=1)
                if split_text[0] != "":
                    new_node = TextNode(split_text[0], TextType.TEXT)
                    final_list.append(new_node)
                link_node = TextNode(anchor_text, TextType.LINK, url)
                final_list.append(link_node)
                remaining_text = split_text[1]
            if remaining_text != "":
                new_node = TextNode(remaining_text, TextType.TEXT)
                final_list.append(new_node)
    return final_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_link = split_nodes_link(split_image)
    return split_link




