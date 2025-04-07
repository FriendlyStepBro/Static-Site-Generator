import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_full_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node, node2)
    
    def test_to_string_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        text = "TextNode(This is a text node, bold, None)"
        self.assertEqual(str(node), text)

    def test_to_string(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        text = "TextNode(This is a text node, bold, https://google.com)"
        self.assertEqual(str(node), text)
        


if __name__ == "__main__":
    unittest.main()