import unittest
from htmlnode import ParentNode, LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_eq_tag_child_props(self):
        child_node_1 = LeafNode("span", "child")
        props1 = {
            "id": "div-1"
        }
        node = ParentNode("div", child_node_1, props1)

        child_node_2 = LeafNode("span", "child")
        props2 = {
            "id": "div-1"
        }
        node2 = ParentNode("div", child_node_2, props2)
        self.assertEqual(node, node2)

    def test_not_eq_tag_child(self):
        child_node_1 = LeafNode("span", "child")
        node = ParentNode("div", child_node_1)

        child_node_2 = LeafNode("p", "child text")
        node2 = ParentNode("div", child_node_2)
        self.assertNotEqual(node, node2)

    def test_not_eq_tag_child_props(self):
        child_node_1 = LeafNode("span", "child")
        props1 = {
            "id": "div-1"
        }
        node = ParentNode("div", child_node_1, props1)

        child_node_2 = LeafNode("span", "child")
        props2 = {
            "id": "div-2"
        }
        node2 = ParentNode("div", child_node_2, props2)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()