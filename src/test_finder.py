import unittest
from finder import extract_markdown_images, extract_markdown_links

class TestFinder(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            'Visit [GitHub](https://github.com).'
        )
        self.assertListEqual([("GitHub", "https://github.com")], matches)