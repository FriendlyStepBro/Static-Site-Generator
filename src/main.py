import os
import sys
import shutil
from textnode import *
from functions import generate_page, generate_pages_recursive

# New recursive function to copy a directory
def copy_dir(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Deleted {dst}")
    os.mkdir(dst)
    print(f"Created directory {dst}")
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        dest_path = os.path.join(dst, item)
        if os.path.isdir(item_path):
            os.mkdir(dest_path)
            print(f"Created directory {dest_path}")
            copy_dir(item_path, dest_path)
        else:
            shutil.copy(item_path, dest_path)
            print(f"Copied file {item_path} to {dest_path}")

def main():
    # Get basepath from CLI argument; default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print('Basepath:', basepath)
    print('hello world')
    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test_node)
    # Compute paths relative to this file
    project_root = os.path.join(os.path.dirname(__file__), "..")
    static_dir = os.path.join(project_root, "static")
    docs_dir = os.path.join(project_root, "docs")  # changed from public to docs
    print(f"Copying from {static_dir} to {docs_dir}")
    copy_dir(static_dir, docs_dir)
    # Generate pages recursively for every markdown file in the content directory; pass basepath
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()