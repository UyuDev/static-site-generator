from copy_static import copy_static
from gen_content import generate_page

def main():
    source_dir = "static"
    target_path = "public"
    template = "template.html"
    index = "content/index.md"
    target_index = "public/index.html"
    copy_static(source_dir, target_path)
    generate_page(index, template, target_index)


if __name__ == "__main__":
    main()