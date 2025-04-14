import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        text = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), text)
    
    def test_to_html_no_props(self):
        node = LeafNode('p', 'This is a line of test value.')
        text = "<p>This is a line of test value.</p>"
        self.assertEqual(node.to_html(), text)
        
    def test_to_html_prop(self):
        node = LeafNode('a', 'This is a test for props.', {'href':'https://google.com'})
        text = '<a href="https://google.com">This is a test for props.</a>'
        self.assertEqual(node.to_html(), text)

    def test_to_html_props(self):
        node = LeafNode('a', 'This is a line of test value with multiple props.', {'href':'https://google.com', 'target':'_top'})
        text = '<a href="https://google.com" target="_top">This is a line of test value with multiple props.</a>'
        self.assertEqual(node.to_html(), text)
    
    def test_to_html_no_value(self):
        with self.assertRaises(ValueError):
            test_node = LeafNode('a', props={'href':'https://google.com', 'target':'_top'})
            test_node.to_html()
    
    def test_to_html_no_tag(self):
        node = LeafNode(value='This is a line of test value.')
        text = "This is a line of test value."

    def test_textnode_to_htmlnode_exception(self):
        with self.assertRaisesRegex(Exception, "text_type not in TextType"):
            text_node = TextNode('test', TextType.LINK)
            text_node.text_type = 'links'
            LeafNode.text_node_to_html_node(text_node)

    def test_textnode_to_htmlnode_normal(self):
        text_node = TextNode('This is a normal text test.', TextType.NORMAL)
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is a normal text test.")

    def test_textnode_to_htmlnode_bold(self):
        text_node = TextNode('This is a bold text test.', TextType.BOLD)
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>This is a bold text test.</b>")

    def test_textnode_to_htmlnode_italic(self):
        text_node = TextNode('This is a italic text test.', TextType.ITALIC)
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>This is a italic text test.</i>")

    def test_textnode_to_htmlnode_code(self):
        text_node = TextNode('This is a code text test.', TextType.CODE)
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>This is a code text test.</code>")
        
    def test_textnode_to_htmlnode_link(self):
        text_node = TextNode('This is a link text test.', TextType.LINK, 'https://google.com')
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://google.com">This is a link text test.</a>')
        
    def test_textnode_to_htmlnode_image(self):
        text_node = TextNode('This is an image test.', TextType.IMAGE, 'https://google.com')
        html_node = LeafNode.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {'src':'https://google.com', 'alt':'This is an image test.'})
        self.assertEqual(html_node.value, None)
        


if __name__ == "__main__":
    unittest.main()