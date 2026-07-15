from copy_static import copy_static
from gen_content import generate_pages_recursive

def main():
    source_dir = "static"
    target_path = "public"
    template = "template.html"
    origin_dir = "content"
    target_dir = "public"
    copy_static(source_dir, target_path)
    generate_pages_recursive(origin_dir, template, target_dir)


if __name__ == "__main__":
    main()