from textnode import TextNode, TextType
from copy_static import copy_static

def main():
    source_dir = "static"
    target_path = "public"
    copy_static(source_dir, target_path)
    


if __name__ == "__main__":
    main()