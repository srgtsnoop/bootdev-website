import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_whitespace(self):
        self.assertEqual(
            extract_title("#    Tolkien Fan Club    "),
            "Tolkien Fan Club",
        )

    def test_ignores_h2(self):
        markdown = """
## Not the title

# Actual Title

Some content
"""
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_no_h1(self):
        markdown = """
## Heading 2

### Heading 3
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
