import unittest
from functions import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_valid_title(self):
        md = "# Hello World\nSome other content"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_with_spaces(self):
        md = "#    Leading and trailing   "
        self.assertEqual(extract_title(md), "Leading and trailing")

    def test_extract_no_title(self):
        md = "No header here\nJust text"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue("No h1 header found" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
