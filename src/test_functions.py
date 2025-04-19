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
    
    def test_extract_markdown_image_no_surround(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = functions.extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



class Test_extract_markdown_link(unittest.TestCase):
    def test_extract_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = functions.extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


class Test_split_nodes_image(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes
        )


class Test_split_nodes_link(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.NORMAL),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes
        )


class Test_text_to_textnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        results = functions.text_to_textnodes(text)
        self.assertListEqual(results, expected)


class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_blocks_simple(self):
        md = "Block 1\n\nBlock 2\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        result = functions.markdown_to_blocks(md)
        self.assertListEqual(result, expected)
    
    def test_markdown_blocks_with_extra_newlines(self):
        md = "\n\nBlock A\n\nBlock B\n\n"
        expected = ["Block A", "Block B"]
        result = functions.markdown_to_blocks(md)
        self.assertListEqual(result, expected)
    
    def test_markdown_blocks_multiline_block(self):
        md = "Line 1\nLine 2\n\nLine 3\nLine 4"
        expected = ["Line 1\nLine 2", "Line 3\nLine 4"]
        result = functions.markdown_to_blocks(md)
        self.assertListEqual(result, expected)
    
    def test_markdown_blocks_with_example_md_text(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
    """
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ]
        result = functions.markdown_to_blocks(md)
        self.assertListEqual(result, expected)