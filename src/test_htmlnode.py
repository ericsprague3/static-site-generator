import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_tag_value(self):
        node = HTMLNode("h1", "Heading 1")
        node2 = HTMLNode("h1", "Heading 1")
        self.assertEqual(node, node2)

    def test_eq_tag_value_children_with_props(self):
        children1 = [
            HTMLNode("a", "Link 1", None, {
                "href": "https://www.google.com"
            })
        ]
        node = HTMLNode("h1", "Heading 1", children1)

        children2 = [
            HTMLNode("a", "Link 1", None, {
                "href": "https://www.google.com"
            })
        ]
        node2 = HTMLNode("h1", "Heading 1", children2)
        self.assertEqual(node, node2)

    def test_eq_tag_value_props(self):
        props1 = {
            "aria-label": "Close dialog"
        }
        node = HTMLNode("button", "X", None, props1)

        props2 = {
            "aria-label": "Close dialog"
        }
        node2 = HTMLNode("button", "X", None, props2)
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        node = HTMLNode("h2", "Heading 1")
        node2 = HTMLNode("h1", "Heading 1")
        self.assertNotEqual(node, node2)
    
    def test_not_eq_value(self):
        node = HTMLNode("p", "This is some text in paragraph")
        node2 = HTMLNode("p", "This is some text in a different paragraph")
        self.assertNotEqual(node, node2)

    def test_not_eq_children(self):
        children1 = [
            HTMLNode("p", "paragraph 1"),
            HTMLNode("p", "paragraph 2")
        ]
        node = HTMLNode("h1", "Heading 1", children1)
        
        children2 = [
            HTMLNode("p", "paragraph 3"),
            HTMLNode("p", "paragraph 4")
        ]
        node2 = HTMLNode("h1", "Heading 1", children2)
        self.assertNotEqual(node, node2)

    def test_not_eq_props(self):
        props1 = {
            "href": "https://www.goggle.com"
        }
        node = HTMLNode("h1", "Heading 1", None, props1)

        props2 = {
            "href": "https://www.google.com"
        }
        node2 = HTMLNode("h1", "Heading 1", None, props2)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()