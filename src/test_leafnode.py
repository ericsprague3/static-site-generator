import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_eq_tag_value(self):
        node = LeafNode("h1", "Heading 1")
        node2 = LeafNode("h1", "Heading 1")
        self.assertEqual(node, node2)

    def test_eq_tag_value_props(self):
        props1 = {
            "aria-label": "Close dialog"
        }
        node = LeafNode("button", "X", props1)

        props2 = {
            "aria-label": "Close dialog"
        }
        node2 = LeafNode("button", "X", props2)
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        node = LeafNode("h2", "Heading 1")
        node2 = LeafNode("h1", "Heading 1")
        self.assertNotEqual(node, node2)
    
    def test_not_eq_value(self):
        node = LeafNode("p", "This is some text in paragraph")
        node2 = LeafNode("p", "This is some text in a different paragraph")
        self.assertNotEqual(node, node2)

    def test_not_eq_props(self):
        props1 = {
            "href": "https://www.goggle.com"
        }
        node = LeafNode("h1", "Heading 1", props1)

        props2 = {
            "href": "https://www.google.com"
        }
        node2 = LeafNode("h1", "Heading 1", props2)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()