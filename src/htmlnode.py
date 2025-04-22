import functools

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        result = f"<{self.tag}"
        props = self.props_to_html()
        result += props
        result += ">"
        for node in self.children:
            result += node.to_html
        result += f"</{self.tag}>"

    def props_to_html(self):
        result = ""
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