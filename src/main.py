from copy_static import copy_static
from gen_content import generate_pages_recursive
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    source_dir = "static"
    output_dir = "docs"
    template = "template.html"
    origin_dir = "content"
    copy_static(source_dir, output_dir)
    generate_pages_recursive(origin_dir, template, output_dir, basepath)


if __name__ == "__main__":
    main()