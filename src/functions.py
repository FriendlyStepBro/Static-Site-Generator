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