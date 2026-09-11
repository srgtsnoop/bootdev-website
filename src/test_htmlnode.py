import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Click me!",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(tag="p", value="Hello, world!", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode(
            tag="p",
            value="Hello, world!",
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="Hello, world!",
            children=None,
            props={"class": "primary"},
        )
        self.assertIn("p", repr(node))
        self.assertIn("Hello, world!", repr(node))
        self.assertIn("primary", repr(node))

    def test_children(self):
        child = HTMLNode(tag="span", value="child text")
        parent = HTMLNode(tag="div", children=[child])
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].tag, "span")


if __name__ == "__main__":
    unittest.main()
