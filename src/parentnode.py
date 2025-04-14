from functools import reduce

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Node is missing value")
        if not self.children:
            raise ValueError("Node contains no children")
        
        if self.props:
            prop_to_html = lambda item: f' {item[0]}="{item[1]}"'
            acc_props = lambda acc, string: acc + string
            print(self.props)
            props = reduce(acc_props, list(map(prop_to_html, self.props.items())), "")
        else:
            props = ""

        leafs_to_html = lambda node: node.to_html()
        leafs_to_string = lambda acc, string: acc + string
        children = reduce(leafs_to_string, map(leafs_to_html, self.children), "")

        return f"<{self.tag}{props}>{children}</{self.tag}>"
