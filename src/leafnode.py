from functools import reduce

from htmlnode import HTMLNode
from textnode import TextNode, TextType

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.tag == 'img':  # Allow image nodes to have value None
            if self.props:
                prop_to_html = lambda item: f' {item[0]}="{item[1]}"'
                acc_props = lambda acc, string: acc + string
                props = reduce(acc_props, list(map(prop_to_html, self.props.items())), "")
            else:
                props = ""
            return f"<{self.tag}{props}></{self.tag}>"
        else:
            if self.value is None:
                raise ValueError()
            if not self.tag:
                return self.value
            if self.props:
                prop_to_html = lambda item: f' {item[0]}="{item[1]}"'
                acc_props = lambda acc, string: acc + string
                props = reduce(acc_props, list(map(prop_to_html, self.props.items())), "")
            else:
                props = ""
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def text_node_to_html_node(text_node):
        if type(text_node.text_type) is not TextType:
            raise Exception("text_type not in TextType")
        match text_node.text_type:
            case TextType.NORMAL:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode('b', text_node.text)
            case TextType.ITALIC:
                return LeafNode('i', text_node.text)
            case TextType.CODE:
                return LeafNode('code', text_node.text)
            case TextType.LINK:
                return LeafNode('a', text_node.text, {'href': text_node.url})
            case TextType.IMAGE:
                # Set value to None, as expected by tests.
                return LeafNode('img', None, {'src': text_node.url, 'alt': text_node.text})
