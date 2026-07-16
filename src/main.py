from copy_static import copy_static
from gen_content import generate_pages_recursive
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    source_dir = "static"
    target_path = "public"
    template = "template.html"
    origin_dir = "content"
    target_dir = "public"
    copy_static(source_dir, target_path)
    generate_pages_recursive(origin_dir, template, target_dir, basepath)


if __name__ == "__main__":
    main()