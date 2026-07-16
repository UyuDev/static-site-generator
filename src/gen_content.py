from markdown_blocks import extract_title, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os



def generate_page(from_path: str, template_path: str, dest_path: str, basepath):
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
    replace_href = replace_content.replace('href="/', f'href="{basepath}')
    replace_src = replace_href.replace('src="/', f'src="{basepath}')
    check_directories(dest_path)
    with open(dest_path, "w") as file:
        file.write(replace_src)

def check_directories(target_path: str):
    parent_dir = os.path.dirname(target_path)
    if parent_dir != "":
        os.makedirs(parent_dir, exist_ok=True)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Checking items in directory: {dir_path_content}")
    for item_name in os.listdir(dir_path_content):
        print(f"Checking item: {item_name}")
        full_path = os.path.join(dir_path_content, item_name)
        print(f"Full path: {full_path}")
        print(f"Checking if {full_path} is a file: {os.path.isfile(full_path)}")
        if os.path.isfile(full_path):
            print(f"Checking if {item_name} is a .md file")
            new_item_name = item_name
            if ".md" in item_name:
                print(f"Changing from .md to .html file")
                new_item_name = new_item_name.replace(".md", ".html")
            print(f"Generating a new file for {item_name} in directory:{dest_dir_path}")
            new_dest_path = os.path.join(dest_dir_path, new_item_name)
            generate_page(full_path, template_path, new_dest_path, basepath)
        print(f"Checking if {full_path} is a directory: {os.path.isdir(full_path)}")
        if os.path.isdir(full_path):
            new_dest_path = os.path.join(dest_dir_path, item_name)
            print(f"New destination path: {new_dest_path}")
            os.mkdir(new_dest_path)
            print(f"Making new directory: {new_dest_path}")
            print(f"Recursively calling generate_pages_recursive with source: {full_path} and target: {new_dest_path}")
            generate_pages_recursive(full_path, template_path, new_dest_path, basepath)