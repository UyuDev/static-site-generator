from markdown_blocks import extract_title, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os



def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown_contents = file.read()
    with open(template_path, "r") as file:
        template_contents = file.read()
    title = extract_title(markdown_contents)
    parent_node = markdown_to_html_node(markdown_contents)
    html_text = parent_node.to_html()
    replace_title = template_contents.replace("{{ Title }}", title)
    replace_content = replace_title.replace("{{ Content }}", html_text)
    check_directories(dest_path)
    with open(dest_path, "w") as file:
        file.write(replace_content)

def check_directories(target_path: str):
    parent_dir = os.path.dirname(target_path)
    if parent_dir != "":
        os.makedirs(parent_dir, exist_ok=True)