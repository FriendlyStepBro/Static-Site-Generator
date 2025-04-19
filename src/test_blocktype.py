import unittest
from blocktype import BlockType, get_block_type

class TestBlockNodeFunctions(unittest.TestCase):
    def test_is_heading(self):
        from blocktype import is_heading
        # Normal: Has a hash and a space after it.
        self.assertTrue(is_heading("# Heading"))
        # Edge: No space after hashes should fail.
        self.assertFalse(is_heading("###Heading"))
        # Edge: Empty string.
        self.assertFalse(is_heading(""))


    def test_is_code(self):
        from blocktype import is_code
        # Normal: Proper code block with triple backticks start and end.
        code_block = "```python\nprint('Hello')\n```"
        self.assertTrue(is_code(code_block))
        # Edge: Missing the ending triple backticks.
        incomplete_code = "```python\nprint('Hello')"
        self.assertFalse(is_code(incomplete_code))


    def test_is_quote(self):
        from blocktype import is_quote
        # Normal: Every line starts with '>'.
        quote_block = "> Quote one\n> Quote two"
        self.assertTrue(is_quote(quote_block))
        # Edge: One line not starting with '>' fails.
        bad_quote = "> Quote one\nQuote two"
        self.assertFalse(is_quote(bad_quote))


    def test_is_unordered_list(self):
        from blocktype import is_unordered_list
        # Normal: Every line starts with "- ".
        unordered = "- Item 1\n- Item 2"
        self.assertTrue(is_unordered_list(unordered))
        # Edge: One line missing the dash.
        bad_unordered = "- Item 1\nItem 2"
        self.assertFalse(is_unordered_list(bad_unordered))


    def test_is_ordered_list(self):
        from blocktype import is_ordered_list
        # Normal: Lines start with an incrementing number followed by ". ".
        ordered = "1. First item\n2. Second item\n3. Third item"
        self.assertTrue(is_ordered_list(ordered))
        # Edge: Sequence is incorrect.
        bad_ordered = "1. First item\n3. Second item"
        self.assertFalse(is_ordered_list(bad_ordered))
        # Edge: Non-numeric marker.
        non_numeric = "A. First item\n2. Second item"
        self.assertFalse(is_ordered_list(non_numeric))


    def test_get_block_type_heading(self):
        self.assertEqual(get_block_type("# Heading Example"), BlockType.HEADING)


    def test_get_block_type_code(self):
        code_block = "```python\nprint('Hello')\n```"
        self.assertEqual(get_block_type(code_block), BlockType.CODE)


    def test_get_block_type_quote(self):
        quote_block = "> Quote one\n> Quote two"
        self.assertEqual(get_block_type(quote_block), BlockType.QUOTE)


    def test_get_block_type_unordered(self):
        unordered = "- Item 1\n- Item 2"
        self.assertEqual(get_block_type(unordered), BlockType.UNORDERED_LIST)


    def test_get_block_type_ordered(self):
        ordered = "1. First item\n2. Second item"
        self.assertEqual(get_block_type(ordered), BlockType.ORDERED_LIST)


    def test_get_block_type_default(self):
        default_text = "Some normal text without special markers."
        self.assertEqual(get_block_type(default_text), BlockType.PARAGRAPH)
