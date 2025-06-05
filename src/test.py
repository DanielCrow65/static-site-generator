import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq_property(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_text(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is also a test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a test node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a test node", TextType.BOLD, "https://www.wikipedia.org")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_two(self):
        node = TextNode("This is a test node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a test node", TextType.BOLD,)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()