import unittest
from textnode import TextNode, TextType
from delimiter import (
    split_nodes_delimiter, split_nodes_image, split_nodes_link, 
    text_to_textnodes, markdown_to_blocks
)


class TestTextNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("**This is a bold node**", TextType.BOLD)
        node3 = TextNode("This is a second text node with **bold value** and trailing text", TextType.TEXT)
        old_nodes = [ node, node2, node3 ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], node)
        self.assertEqual(new_nodes[1], node2)
        self.assertEqual(new_nodes[2], TextNode("This is a second text node with ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("bold value", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" and trailing text", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("_This is a italic node_", TextType.ITALIC)
        node3 = TextNode("This is a second text node with _italic value_ and trailing text", TextType.TEXT)
        old_nodes = [ node, node2, node3 ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], node)
        self.assertEqual(new_nodes[1], node2)
        self.assertEqual(new_nodes[2], TextNode("This is a second text node with ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic value", TextType.ITALIC))
        self.assertEqual(new_nodes[4], TextNode(" and trailing text", TextType.TEXT))

    def test_code(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("`This is a code node`", TextType.CODE)
        node3 = TextNode("This is a second text node with `code block` and trailing text", TextType.TEXT)
        old_nodes = [ node, node2, node3 ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[0], node)
        self.assertEqual(new_nodes[1], node2)
        self.assertEqual(new_nodes[2], TextNode("This is a second text node with ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" and trailing text", TextType.TEXT))

    def test_bold_invalid_markdown(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("**This is a bold node**", TextType.BOLD)
        node3 = TextNode("This is a second text node with **bold value and trailing text", TextType.TEXT)
        old_nodes = [ node, node2, node3 ]
        try:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
            assert False, "ValueError was not raised"
        except ValueError as e:
            self.assertIsInstance(e, ValueError)
            self.assertEqual(str(e), f"Invalid markdown, delimiter ** not properly closed")

    def test_bold_invalid_markdown_confirm_message(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("**This is a bold node**", TextType.BOLD)
        node3 = TextNode("This is a second text node with **bold value and trailing text", TextType.TEXT)
        old_nodes = [ node, node2, node3 ]
        try:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
            assert False, "ValueError was not raised"
        except ValueError as e:
            self.assertIsInstance(e, ValueError)
            self.assertNotEqual(str(e), f"Invalid markdown, delimiter ` not properly closed")

    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(test_text)
        confirm_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(output, confirm_list)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()