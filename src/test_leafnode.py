import unittest

from leafnode import LeafNode

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
        
        


if __name__ == "__main__":
    unittest.main()