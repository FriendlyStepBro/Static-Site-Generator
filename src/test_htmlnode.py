import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_to_html_exception(self):
         with self.assertRaises(NotImplementedError):
             test_obj = HTMLNode()
             test_obj.to_html()
        
    def test_props_to_html(self):
        node = HTMLNode('p', 'test', None, {'href': 'https://google.com', 'target': '_blank',})
        text = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), text)

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
    
    
if __name__ == "__main__":
    unittest.main()