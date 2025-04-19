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
            if text[i] == '!' and text[i+1] == '[':
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
        print(nodes)
    nodes = split_nodes_image(nodes)
    print(nodes)
    nodes = split_nodes_link(nodes)
    print(nodes)
    return nodes


def markdown_to_blocks(markdown):
    import re
    pattern = r'(?:^|\n\n)(.*?)(?=\n\n|$)'
    blocks = re.findall(pattern, markdown, flags=re.DOTALL)
    return [block.strip() for block in blocks if block.strip()]