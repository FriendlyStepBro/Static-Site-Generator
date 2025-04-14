import unittest

from textnode import TextNode, TextType
import functions

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_empty_node(self):
        node = TextNode("", TextType.NORMAL)
        expected = []
        self.assertEqual(functions.split_nodes_delimiter([node], "_", TextType.BOLD), expected)

    def test_single_node_italic(self):
        node = TextNode("This is an _italic text_ test node", TextType.NORMAL)
        expected = [
            TextNode("This is an ", TextType.NORMAL),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" test node", TextType.NORMAL),
        ]
        result = functions.split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, expected)

    
    def test_multi_node_no_delimiter(self):
        nodes = [
            TextNode("This is a test `node`", TextType.NORMAL),
            TextNode("This is also a test **node**", TextType.NORMAL),
            TextNode("This is yet _another_ test node", TextType.NORMAL),
            TextNode("This is a _embedded **text** node_", TextType.NORMAL)
        ]
        expected = [
            TextNode("This is a test `node`", TextType.NORMAL),
            TextNode("This is also a test ", TextType.NORMAL),
            TextNode("node", TextType.BOLD),
            TextNode("This is yet _another_ test node", TextType.NORMAL),
            TextNode("This is a _embedded ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" node_", TextType.NORMAL),
        ]
        result = functions.split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, expected)

class Test_extract_markdown_image(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = functions.extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = functions.extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

class Test_extract_markdown_link(unittest.TestCase):
    def test_extract_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = functions.extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)