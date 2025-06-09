import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion import text_node_to_html_node, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    # TEXT NODE TESTS
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
    
    # HTML NODE TESTS
    def test_prop_output(self):
        my_dict = {"href": "www.google.com", "target": "_blank"}
        node = HTMLNode('a', "Test link here", None, my_dict)
        result = node.props_to_html()
        result2 = ' href="www.google.com" target="_blank"'
        self.assertEqual(result, result2)
    
    def test_prop_output_none(self):
        node = HTMLNode("h1", "This is a test h1 tag", None)
        result = node.props_to_html()
        result2 = ""
        self.assertEqual(result, result2)

    def test_prop_output_empty_string(self):
        node = HTMLNode("footer", "This is a test footer", None, "")
        result = node.props_to_html()
        result2 = ""
        self.assertEqual(result, result2)

    def test_prop_output_empty_dict(self):
        node = HTMLNode("header", "This is a test header", None, {})
        result = node.props_to_html()
        result2 = ""
        self.assertEqual(result, result2)

    # LEAF NODE TESTS
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Checks if empty strings or None inputs properly return raw text
    def test_leaf_to_html_empty_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # Checks if error is properly raised from an invalid value
    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)
    
    # Checks if LeafNode properly inherited the props_to_html() method
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click!", {"href": "www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="www.google.com" target="_blank">Click!</a>')

    # PARENT NODE TESTS
    def test_parent_to_html(self):
        child_one = LeafNode("h2","Test Heading")
        child_two = LeafNode('a', "Test line here", {"href": "www.google.com", "target": "_blank"})
        node = ParentNode("body", [child_one, child_two], None)
        self.assertEqual(node.to_html(), '<body><h2>Test Heading</h2><a href="www.google.com" target="_blank">Test line here</a></body>')

    def test_parent_missing_tag(self):
        child_one = LeafNode("div", "Test Div")
        child_two = LeafNode("b", "Test Bold")
        node = ParentNode(None, [child_one, child_two], None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_missing_children(self):
        node = ParentNode("body", None, None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    # A parent node can have an empty list of children, because it can gain some later
    def test_parent_empty_children(self):
        node = ParentNode("body", [], None)
        self.assertEqual(node.to_html(), "<body></body>")

    # Those brackets are necessary, without them it will see an HTMLNode class/child class, not a list!
    def test_parent_nested_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_parent_more_nested_parents(self):
        great_grandchild_node = LeafNode("b", "great_grandchild")
        grandchild_node = ParentNode("span", [great_grandchild_node])
        child_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("body", [child_node])
        self.assertEqual(parent_node.to_html(), "<body><div><span><b>great_grandchild</b></span></div></body>")

    # TEXTNODE TO HTMLNODE TESTS
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("I am feeling bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "I am feeling bold")

    def test_italic(self):
        node = TextNode("I feel a bit tilted", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "I feel a bit tilted")

    def test_code(self):
        node = TextNode("This is a block of code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a block of code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.wikipedia.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props_to_html(), ' href="www.wikipedia.org"')
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "/images/assets/sample.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), ' src="/images/assets/sample.png" alt="This is an image"')

    # The TextNode constructor does not enforce a proper TextType, so it can create an invalid TextNode like this
    def test_invalid_texttype(self):
        node = TextNode("I should not be created", "I am not a valid text type")
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)
    
    # SPLIT NODES DELIMITER TESTS
    def test_split_no_delimiter(self):
        node = TextNode("I am a perfectly normal set of raw text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expectation = [TextNode('I am a perfectly normal set of raw text', TextType.TEXT, None)]
        self.assertEqual(result, expectation)

    def test_split_has_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expectation = [
            TextNode('This is text with a ', TextType.TEXT, None), 
            TextNode('code block', TextType.CODE, None), 
            TextNode(' word', TextType.TEXT, None)
        ]
        self.assertEqual(result, expectation)
    
    def test_split_multichar_delimiter(self):
        node = TextNode("I am a **bolded block** of text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expectation = [
            TextNode("I am a ", TextType.TEXT),
            TextNode("bolded block", TextType.BOLD),
            TextNode(" of text", TextType.TEXT),
        ]
        self.assertEqual(result, expectation)
    
    def test_split_delimiter_start_and_end(self):
        node = TextNode("**I start with a delimiter** and I have **another delimiter at the end**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expectation = [
            TextNode('I start with a delimiter', TextType.BOLD), 
            TextNode(' and I have ', TextType.TEXT),
            TextNode('another delimiter at the end', TextType.BOLD)
        ]
        self.assertEqual(result, expectation)

    def test_split_multiple_inputs(self):
        node1 = TextNode("I am just raw text!", TextType.TEXT)
        node2 = TextNode("I am a piece of italic text!", TextType.ITALIC)
        node3 = TextNode("I am another set of raw text!", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2, node3], "_", TextType.ITALIC)
        expectation = [
            TextNode('I am just raw text!', TextType.TEXT), 
            TextNode('I am a piece of italic text!', TextType.ITALIC), 
            TextNode('I am another set of raw text!', TextType.TEXT)
        ]
        self.assertEqual(result, expectation)

    def test_split_error_no_closing_delimiter(self):
        node = TextNode("I forgot to close my _delimiter, oops!", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()