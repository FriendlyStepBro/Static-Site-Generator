import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode('p', 'test', None, {'href': 'https://google.com', 'target': '_blank',})
        text = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), text)

    def test_empty_props(self):
        # When props is an empty dict, the output should be an empty string.
        node = HTMLNode(tag="div", children=[], props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_numeric_prop_value(self):
        # Non-string property values should be converted to string.
        node = HTMLNode(tag="div", children=[], props={"data-id": 123})
        self.assertEqual(node.props_to_html(), ' data-id="123"')

    def test_to_string(self):
        childnodes = [
            HTMLNode('a', 'testing_a_child', None, {'href': 'https://childOne.com', 'target': '_self'}),
            HTMLNode('b', 'test_bold_text_child', None, {'link': 'ftp://192.168.50.12'})
        ]
        node = HTMLNode('p', 'test', childnodes, {'href': 'https://google.com', 'target': '_blank',})
        text =  "HTMLNode(p, test, ["
        text += "HTMLNode(a, testing_a_child, None, {'href': 'https://childOne.com', 'target': '_self'}), "
        text += "HTMLNode(b, test_bold_text_child, None, {'link': 'ftp://192.168.50.12'})"
        text += "], {'href': 'https://google.com', 'target': '_blank'})"
        self.assertEqual(str(node), text)

    def test_simple_node(self):
        # Simple node without props and children.
        node = HTMLNode(tag="p", children=[])
        self.assertEqual(node.to_html(), "<p></p>")
    
    def test_node_with_props(self):
        # Node with properties.
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"></div>')

    def test_nested_nodes(self):
        # Nested nodes: a div containing a span.
        child = HTMLNode(tag="span", children=[])
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(parent.to_html(), "<div><span></span></div>")
    
    def test_link_node(self):
        # A link node with an href and with a nested span.
        child = HTMLNode(tag="span", children=[])
        link = HTMLNode(tag="a", children=[child], props={"href": "https://example.com"})
        self.assertEqual(link.to_html(), '<a href="https://example.com"><span></span></a>')

    def test_image_node(self):
        # An image node with src and alt; not self-closing per current implementation.
        img = HTMLNode(tag="img", children=[], props={"src": "image.png", "alt": "an image"})
        self.assertEqual(img.to_html(), '<img src="image.png" alt="an image"></img>')

    def test_repr_with_none_children(self):
        # __repr__ should show children as None when it is not provided.
        node = HTMLNode(tag="div", value="sample", children=None, props={"class": "test"})
        expected = "HTMLNode(div, sample, None, {'class': 'test'})"
        self.assertEqual(repr(node), expected)

    def test_props_with_none(self):
        # When props is None, the output should be an empty string.
        node = HTMLNode(tag="div", children=[], props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_text_node_to_html_node_normal(self):
        tn = TextNode("hello", TextType.NORMAL, None)  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "hello")

    def test_text_node_to_html_node_bold(self):
        tn = TextNode("bold text", TextType.BOLD, None)  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_text_node_to_html_node_italic(self):
        tn = TextNode("italic text", TextType.ITALIC, None)  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_text_node_to_html_node_code(self):
        tn = TextNode("code sample", TextType.CODE, None)  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code sample")

    def test_text_node_to_html_node_link(self):
        tn = TextNode("click here", TextType.LINK, "https://example.com")  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        tn = TextNode("an image", TextType.IMAGE, "image.png")  # corrected argument order
        html_node = HTMLNode.text_node_to_html_node(tn)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "an image"})
