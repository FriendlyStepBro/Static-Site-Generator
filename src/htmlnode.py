import functools
from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []  # fixed: ensure children is iterable
        self.props = props if props is not None else {}
    
    def text_node_to_html_node(node: TextNode):
        value = node.text
        url = node.url
        match (node.text_type):
            case TextType.NORMAL:
                tag = 'p'
                return HTMLNode(tag, value)
            case TextType.BOLD:
                tag = 'b'
                return HTMLNode(tag, value)
            case TextType.ITALIC:
                tag = 'i'
                return HTMLNode(tag, value)
            case TextType.CODE:
                tag = 'code'
                return HTMLNode(tag, value)
            case TextType.LINK:
                tag = 'a'
                return HTMLNode(tag, value, None, {"href": url})
            case TextType.IMAGE:
                tag = 'img'
                return HTMLNode(tag, "", None, {"src": url, "alt": value})

    def to_html(self):
        result = f"<{self.tag}{self.props_to_html()}>"
        if self.value is not None:
            result += self.value
        for node in self.children:
            result += node.to_html()
        result += f"</{self.tag}>"
        return result

    def props_to_html(self):
        result = ""
        if not self.props: return result
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        if self.children:
            children = list(map(str, self.children))
            string_concat = lambda acc, string: acc + string + ", "
            children = functools.reduce(string_concat, children, "")
            children = f"[{children[0:-2]}]"
        else:
            children = None
        result = f"HTMLNode({self.tag}, {self.value}, {children}, {self.props})"
        return result