from re import findall

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return [
        new_node for node in old_nodes
        for new_node in (
            [node] if node.text_type != TextType.NORMAL else [
                TextNode(seg, text_type if i % 2 else TextType.NORMAL)
                for i, seg in enumerate(node.text.split(delimiter)) if seg
            ]
        )
    ]


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:  # preserve non-normal nodes
            new_nodes.append(node)
            continue
        text = node.text
        strings = []
        start_index = 0
        i = 0
        while i < len(text):
            # Check that i+1 is in bounds before accessing text[i+1]
            if i < len(text) - 1 and text[i] == '!' and text[i+1] == '[':
                strings.append(text[start_index:i])
                start_index = i
                j = i + 2
                while True:
                    if j >= len(text):  # ensure j is within bounds
                        raise Exception("Search exceeding string range")
                    if text[j] == ')':
                        strings.append(text[start_index:j+1])
                        start_index = j + 1
                        i = start_index
                        break
                    j += 1
            else:
                i += 1
        if start_index < len(text):
            strings.append(text[start_index:])
        for string in strings:
            if string and string[0] == '!':
                text_val, url = extract_markdown_images(string)[0]
                new_nodes.append(TextNode(text_val, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(string, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:  # preserve non-normal nodes
            new_nodes.append(node)
            continue
        text = node.text
        strings = []
        start_index = 0
        i = 0
        while i < len(text):
            if text[i] == '[':
                strings.append(text[start_index:i])
                start_index = i
                j = i+2
                while True:
                    if text[j] == ')':
                        strings.append(text[start_index:j+1])
                        start_index = j + 1
                        i = start_index
                        break
                    elif j >= len(text):
                        raise Exception("Search exceeding string range")
                    j += 1
            i += 1
        if start_index < len(text):
            strings.append(text[start_index:])
        for string in strings:
            if string and string[0] == '[':
                text_val, url = extract_markdown_links(string)[0]
                new_nodes.append(TextNode(text_val, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(string, TextType.NORMAL))
    print(new_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    delimiters = [
        ('**', TextType.BOLD),
        ('_', TextType.ITALIC),
        ('`', TextType.CODE),
    ]
    for delimiter, type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    import re
    pattern = r'(?:^|\n\n)(.*?)(?=\n\n|$)'
    blocks = re.findall(pattern, markdown, flags=re.DOTALL)
    return [block.strip() for block in blocks if block.strip()]


def text_to_children(text):
    # Convert inline markdown text into HTMLNodes using text_to_textnodes and LeafNode conversion.
    from leafnode import LeafNode  # use LeafNode instead of HTMLNode conversion
    children = []
    for tn in text_to_textnodes(text):
        children.append(LeafNode.text_node_to_html_node(tn))
    return children


def markdown_to_html_node(markdown):
    from blocktype import BlockType, get_block_type
    blocks = markdown_to_blocks(markdown)
    root = HTMLNode("div", children=[])
    
    # Helper to process list items, unwrapping a single <p> if needed.
    def process_list_item(content):
        children = text_to_children(content)
        if len(children) == 1 and getattr(children[0], "tag", None) == "p":
            return HTMLNode("li", children[0].value)
        else:
            return HTMLNode("li", None, children=children)
    
    for block in blocks:
        b_type = get_block_type(block)
        if b_type == BlockType.HEADING:
            count = 0
            while count < len(block) and block[count] == "#":
                count += 1
            content = block[count:].strip()
            node = HTMLNode(f"h{count}", content)
        elif b_type == BlockType.CODE:
            lines = block.splitlines()
            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            code_text = "\n".join(lines)
            if not code_text.endswith("\n"):
                code_text += "\n"
            code_node = HTMLNode("code", code_text)
            node = HTMLNode("pre", None, children=[code_node])
        elif b_type == BlockType.QUOTE:
            # Remove '>' markers and extra spaces.
            lines = [line.lstrip("> ").rstrip() for line in block.splitlines()]
            content = " ".join(lines)
            node = HTMLNode("blockquote", content)
        elif b_type == BlockType.UNORDERED_LIST:
            items = []
            for item_line in block.splitlines():
                if item_line.startswith("- "):
                    content = item_line[2:].strip()
                    li_node = process_list_item(content)
                    items.append(li_node)
            node = HTMLNode("ul", None, children=items)
        elif b_type == BlockType.ORDERED_LIST:
            items = []
            for item_line in block.splitlines():
                dot_index = item_line.find(". ")
                if dot_index != -1:
                    content = item_line[dot_index+2:].strip()
                    li_node = process_list_item(content)
                    items.append(li_node)
            node = HTMLNode("ol", None, children=items)
        else:
            # Join paragraph lines with a space.
            block_content = " ".join(block.splitlines())
            children = text_to_children(block_content)
            node = HTMLNode("p", None, children=children)
        root.children.append(node)
    return root


def extract_title(markdown):
    """
    Extract the h1 title from markdown.
    Finds the first line starting with a single '#' followed by a space.
    Raises an Exception if no such header exists.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    """
    Generate an HTML page from a markdown file and an HTML template.
    Placeholders:
      {{ Title }} -> page title extracted from markdown
      {{ Content }} -> HTML converted markdown content
    Then replace any occurrences of:
      href="/    with href="{basepath}
      src="/     with src="{basepath}
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as md_file:
        md_text = md_file.read()
    with open(template_path, "r", encoding="utf-8") as tmpl_file:
        template = tmpl_file.read()
    html_str = markdown_to_html_node(md_text).to_html()
    title = extract_title(md_text)
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)
    content = content.replace('href="/', f'href="{basepath}')
    content = content.replace('src="/', f'src="{basepath}')
    import os
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as out_file:
        out_file.write(content)


# New recursive function to generate HTML pages for all markdown files
import os
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_rel_path = os.path.splitext(relative_path)[0] + ".html"
                dest_path = os.path.join(dest_dir_path, html_rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(markdown_path, template_path, dest_path, basepath)