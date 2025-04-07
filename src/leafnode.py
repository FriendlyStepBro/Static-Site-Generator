from functools import reduce

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        if self.props:
            prop_to_html = lambda item: f' {item[0]}="{item[1]}"'
            acc_props = lambda acc, string: acc + string
            print(self.props)
            props = reduce(acc_props, list(map(prop_to_html, self.props.items())), "")
        else:
            props = ""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"