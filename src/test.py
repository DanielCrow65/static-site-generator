import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from extraction import extract_markdown_images, extract_markdown_links, extract_title
from markdown import BlockType, block_to_block_type

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
    
    """ HTML NODE TESTS """
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

    """ LEAF NODE TESTS """
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

    """ PARENT NODE TESTS """
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

    """ TEXTNODE TO HTMLNODE TESTS """
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
    
    """ SPLIT NODES DELIMITER TESTS """
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
        # Note, TextNode's __eq__ method allows this to work. Otherwise assertListEqual is necessary to pass this test

    def test_split_error_no_closing_delimiter(self):
        node = TextNode("I forgot to close my _delimiter, oops!", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    """ EXTRACT MARKDOWN TESTS """
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expectation = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expectation)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expectation = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(matches, expectation)
    
    def test_extract_empty_text(self):
        matches = extract_markdown_images("This is text with an ![](https://i.imgur.com/zjjcJKZ.png)")
        expectation = [('', 'https://i.imgur.com/zjjcJKZ.png')]
        self.assertListEqual(matches, expectation)

    """ SPLIT IMAGE TESTS """
    # Happy Path (with multiple images in a single node)
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
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )
    
    # Simple Text but no images
    def test_split_images_no_image(self):
        node = TextNode("I am a simple text node with no images!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expectation = [TextNode("I am a simple text node with no images!", TextType.TEXT, None)]
        self.assertListEqual(new_nodes, expectation)

    # Non TEXT TextType
    def test_split_images_nontext(self):
        node = TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expectation = [TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD, None)]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax are right next to each other
    def test_split_images_adjacent(self):
        node = TextNode("I have ![two](https://i.imgur.com/zjjcJKZ.png)![images](https://i.imgur.com/3elNhQu.png) right next to each other!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expectation = [
            TextNode("I have ", TextType.TEXT, None), 
            TextNode("two", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
            TextNode("images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"), 
            TextNode(" right next to each other!", TextType.TEXT, None)]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax are separated only with white space
    def test_split_images_whitespace(self):
        node = TextNode("I have ![two](https://i.imgur.com/zjjcJKZ.png) ![images](https://i.imgur.com/3elNhQu.png) next to each other!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expectation = [
            TextNode("I have ", TextType.TEXT, None), 
            TextNode("two", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
            TextNode("images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"), 
            TextNode(" next to each other!", TextType.TEXT, None)
        ]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax at the start and at the end of the string
    def test_split_images_start_and_end(self):
        node = TextNode("![I start with an image](https://i.imgur.com/zjjcJKZ.png) and I end with ![one too.](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expectation = [
            TextNode("I start with an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and I end with ", TextType.TEXT),
            TextNode("one too.", TextType.IMAGE,"https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(new_nodes, expectation)
    
    # Multiple TextNodes in one input
    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT), 
            TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD),
            TextNode("I am a simple text node with no images!", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        expectation = [
            TextNode("This is text with an ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
            TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD), 
            TextNode("I am a simple text node with no images!", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expectation)

    """ SPLIT LINK TESTS """
    # Happy Path (has multiple links and ends in a link)
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expectation = [
            TextNode("This is text with a link ", TextType.TEXT), 
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" and ", TextType.TEXT), 
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(new_nodes, expectation)

    # Simple Text with no Links
    def test_split_links_no_link(self):
        node = TextNode("I am a simple text node with no links!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expectation = [TextNode("I am a simple text node with no links!", TextType.TEXT)]
        self.assertListEqual(new_nodes, expectation)
    
    # Non TEXT TextType (with a link that should be ignored)
    def test_split_links_nontext(self):
        node = TextNode(
            "**I am not a simple text node, but I am not a [link node](https://www.boot.dev), either!", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        expectation = [
            TextNode("**I am not a simple text node, but I am not a [link node](https://www.boot.dev), either!", TextType.BOLD)
            ]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax at the start of the string
    def test_split_links_start(self):
        node = TextNode("[Boot dev](https://www.boot.dev) is an excellent website!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expectation = [
            TextNode("Boot dev", TextType.LINK, "https://www.boot.dev"), 
            TextNode(" is an excellent website!", TextType.TEXT)
            ]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax are right next to each other
    def test_split_links_adjacent(self):
        node = TextNode("I have [two](https://www.boot.dev)[links](https://www.youtube.com/@bootdotdev) right next to each other.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expectation = [
            TextNode("I have ", TextType.TEXT), 
            TextNode("two", TextType.LINK, "https://www.boot.dev"), 
            TextNode("links", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            TextNode(" right next to each other.", TextType.TEXT)
            ]
        self.assertListEqual(new_nodes, expectation)
    
    # Markdown syntax are separated only with whitespace
    def test_split_links_whitespace(self):
        node = TextNode("I have [two](https://www.boot.dev) [links](https://www.youtube.com/@bootdotdev) on me too!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expectation = [
            TextNode("I have ", TextType.TEXT), 
            TextNode("two", TextType.LINK, "https://www.boot.dev"), 
            TextNode("links", TextType.LINK, "https://www.youtube.com/@bootdotdev"), 
            TextNode(" on me too!", TextType.TEXT)
            ]
        self.assertListEqual(new_nodes, expectation)

    # Multiple TextNodes in one input:
    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT), 
            TextNode("**I am not a simple text node, but not a link node either!**", TextType.BOLD),
            TextNode("I am a simple text node with no links!", TextType.TEXT)
            ]
        new_nodes = split_nodes_link(nodes)
        expectation = [
            TextNode("This is text with a ", TextType.TEXT), 
            TextNode("link", TextType.LINK, "https://www.boot.dev"), 
            TextNode("**I am not a simple text node, but not a link node either!**", TextType.BOLD), 
            TextNode("I am a simple text node with no links!", TextType.TEXT)
            ]
        self.assertListEqual(new_nodes, expectation)

    """ TEXT TO TEXTNODE TESTS"""
    # Happy Path
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expectation = [
            TextNode("This is ", TextType.TEXT), TextNode("text", TextType.BOLD), TextNode(" with an ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), TextNode(" word and a ", TextType.TEXT), TextNode("code block", TextType.CODE), 
            TextNode(" and an ", TextType.TEXT), TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), 
            TextNode(" and a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev")
            ]
        self.assertListEqual(result, expectation)

    # Layered delimiters are not supported so should only capture the bolded text, not the italic text layered inside
    def test_text_to_textnode_layered_delimiters(self):
        text = "I have **_a bolded italic word_** in me..."
        result = text_to_textnodes(text)
        expectation = [
            TextNode("I have ", TextType.TEXT), 
            TextNode("_a bolded italic word_", TextType.BOLD), 
            TextNode(" in me...", TextType.TEXT)
        ]
        self.assertListEqual(result, expectation)

    # Directly adjacent different delimiters and with whitespace
    def test_text_to_textnode_adjacent(self):
        text = "_I happen_ **to have** `adjacent delimiters` and really **adjacent**_ones_`too`"
        result = text_to_textnodes(text)
        expectation = [
            TextNode("I happen", TextType.ITALIC), TextNode(" ", TextType.TEXT), TextNode("to have", TextType.BOLD), 
            TextNode(" ", TextType.TEXT), TextNode("adjacent delimiters", TextType.CODE), TextNode(" and really ", TextType.TEXT), 
            TextNode("adjacent", TextType.BOLD), TextNode("ones", TextType.ITALIC), TextNode("too", TextType.CODE)
        ]
        self.assertEqual(result, expectation)

    """ MARKDOWN TO BLOCK TESTS """
    # Happy Path
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        result = markdown_to_blocks(md)
        expectation = [
            'This is **bolded** paragraph', 
            'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line', 
            '- This is a list\n- with items'
            ]
        self.assertEqual(result, expectation)

    # Excess newlines produce empty blocks that must be eliminated
    def test_markdown_to_blocks_empty_block(self):
        md = """
My paragraph is quite nice.



But there might be
some extra space that does not belong there?

How vexing.
"""
        result = markdown_to_blocks(md)
        expectation = [
            'My paragraph is quite nice.', 
            'But there might be\nsome extra space that does not belong there?', 
            'How vexing.'
            ]
        self.assertEqual(result, expectation)
    
    # Blank newlines at the start and the end of the input must be ignored (white spaces are empty)
    def test_markdown_to_blocks_empty_start_and_end(self):
        md = """


I have an empty line before me.

I have a two white spaces behind me.
 
 
"""
        result = markdown_to_blocks(md)
        expectation = [
            'I have an empty line before me.', 
            'I have a two white spaces behind me.'
            ]
        self.assertEqual(result, expectation)
    
    # No blank spaces at all
    def test_markdown_to_blocks_no_blank(self):
        md = """
I have some strings, to pull me down
but I got no blank spaces on me
Just a continuous stream
of issue.
"""
        result = markdown_to_blocks(md)
        expectation = [
            'I have some strings, to pull me down\nbut I got no blank spaces on me\nJust a continuous stream\nof issue.'
            ]
        self.assertEqual(result, expectation)
    
    # Just an empty string
    def test_markdown_to_blocks_empty_string(self):
        md = ""
        result = markdown_to_blocks(md)
        expectation = []
        self.assertEqual(result, expectation)

    # Only whitespace inputs (spaces, tabs, newlines)
    def test_markdown_to_blocks_only_whitespace(self):
        md = """


 
 

    

"""
        result = markdown_to_blocks(md)
        expectation = []
        self.assertEqual(result, expectation)

    """ BLOCK TO BLOCK TYPE TESTS """
    def test_block_to_blocktype_heading(self):
        md = "# I am a valid heading!"
        result = block_to_block_type(md)
        expectation = BlockType.HEAD
        self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_quote(self):
        md = """
> I am a valid quote
> No really, I am!
> Don't dare doubt me!
""".strip()
        result = block_to_block_type(md)
        expectation = BlockType.QUOT
        self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_code(self):
        md = "```I am a code block, yes sir!```"

        result = block_to_block_type(md)
        expectation = BlockType.CODE
        self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_unordered_list(self):
        md = """
- I am a list
- I have no order
- Let chaos reign!
""".strip()
        result = block_to_block_type(md)
        expectation = BlockType.ULIST
        self.assertEqual(result, expectation)
    
    # Even if the sequencing is not strictly followed, it is a valid ordered list
    def test_block_to_blocktype_ordered_list(self):
        md = """
1. I am a list
2. I demand order
3. Laws will save this accursed land
6. And I shall forever remain lawful, even if I break sequence!
""".strip()
        result = block_to_block_type(md)
        expectation = BlockType.OLIST
        self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_invalid_header_no_whitespace(self):
        md = "######I was supposed to be a heading block, but I forgot my whitespace. I beg forgiveness"
        result = block_to_block_type(md)
        expectation = BlockType.PARA
        self.assertEqual(result, expectation)

    def test_block_to_blocktype_invalid_header_extra(self):
        md = "####### I was supposed to be a heading block, but I think I have too many # symbols..."
        result = block_to_block_type(md)
        expectation = BlockType.PARA
        self.assertEqual(result, expectation)

    def test_block_to_blocktype_invalid_quote(self):
        md = "> I am a valid quote\n> No really, I am!\nTrust me, would I steer you wrong?"
        result = block_to_block_type(md)
        expectation = BlockType.PARA
        self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_invalid_unordered_list(self):
            md = """
- I am a list
I have no order
- But at what cost?
""".strip()
            result = block_to_block_type(md)
            expectation = BlockType.PARA
            self.assertEqual(result, expectation)
    
    def test_block_to_blocktype_invalid_ordered_list(self):
        md = """
2. I am a list
3. I demand order
- ...But I have been rendered fallible
""".strip()
        result = block_to_block_type(md)
        expectation = BlockType.PARA
        self.assertEqual(result, expectation)
        
    def test_block_to_blocktype_empty_string(self):
        md = ""
        result = block_to_block_type(md)
        expectation = BlockType.PARA
        self.assertEqual(result, expectation)
        
    """ BLOCK TO HTML TESTS """
    # Header Happy Path
    def test_block_to_html_header(self):
        md = """
# I am a header block

## And so am I!

### Me too!

#### Don't forget about me!

##### I'm not late to the party, am I?

###### Hey wait for me!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>I am a header block</h1><h2>And so am I!</h2><h3>Me too!</h3><h4>Don't forget about me!</h4><h5>I'm not late to the party, am I?</h5><h6>Hey wait for me!</h6></div>"
        )
    
    def test_block_to_html_header_with_inline_markdown(self):
        md = "## This is a **bold** header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is a <b>bold</b> header</h2></div>")
    
    # Blocks are separated by 2 newlines, so a header with a single internal newline is still one block
    # Headers are treated like one line in HTML, so they must be replaced with a whitespace.
    # This test checks if the replacement is being done correctly
    def test_block_to_html_header_with_internal_newline(self):
        md = """
# This is a
multi-line header
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a multi-line header</h1></div>")

    # A Paragraph block should correctly parse inline markdown and turn newlines into spaces
    # because a paragraph block is processed only as a single line
    # This tests also process inline markdown
    def test_block_to_html_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # A Code block should not process inline markdown
    def test_block_to_html_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    # An Unordered List block allows * as a markdown indicator
    def test_block_to_html_unordered_list_variants(self):
        md = """
- Item one
* Item two
- Item three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        self.assertEqual(html, expected_html)
        
    # For an Ordered List, it does not matter that it is not actually ordered in the markdown input
    # We only need to check if it follows a valid ordered list format (i.e. number, period, whitespace)
    # A browser will properly reinterpret the html into an *actually ordered* list
    def test_block_to_html_ordered_list_broken_sequence_input(self):
        md = """
1. Alpha
2. Beta
10. Gamma
11. Delta
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ol><li>Alpha</li><li>Beta</li><li>Gamma</li><li>Delta</li></ol></div>"
        self.assertEqual(html, expected_html)
    
    def test_block_to_html_mixed_blocks(self):
        md = """
# Welcome

This is a paragraph.

* List item one
* List item two

> This is a quote.

```
some_code = "hello"
```

## Subheading

Another paragraph here.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>Welcome</h1><p>This is a paragraph.</p><ul><li>List item one</li><li>List item two</li></ul><blockquote>This is a quote.</blockquote><pre><code>some_code = \"hello\"\n</code></pre><h2>Subheading</h2><p>Another paragraph here.</p></div>"
        self.assertEqual(html, expected_html)
    
    def test_block_to_html_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    # Escape characters like \n for new lines or \t for tabs are empty inputs ignored by markdown
    def test_block_to_html_whitespace_markdown(self):
        md = "   \n\n\t"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    """ EXTRACT TITLE TESTS """
    def test_extract_title(self):
        result = extract_title("# Hello")
        expectation = "Hello"
        self.assertEqual(result, expectation)

    # Should only grab the first valid title
    def test_extract_title_multiple_titles(self):
        md = """
- I am not a title
# But I am!
# I am also valid, but I wasn't here first...
"""
        result = extract_title(md)
        expectation = "But I am!"
        self.assertEqual(result, expectation)

    def test_extract_title_multiline_markdown(self):
        md = """
- I am not a title

> I am not a title either

1. Still not a title

# How about me?

```
I don't think I am a title either
```

My world for a title...
"""
        result = extract_title(md)
        expectation = "How about me?"
        self.assertEqual(result, expectation)

    # Only h1 is acceptable, other header tags are not
    def test_extract_title_invalid_headers(self):
        with self.assertRaises(Exception):
            extract_title("### Hello.")

    def test_extract_title_no_valid_titles(self):
        with self.assertRaises(Exception):
            extract_title("- Not a valid title.")

    # If valid title syntax was found, but it is empty after processing
    def test_extract_title_empty_title(self):
        with self.assertRaises(Exception):
            extract_title("# ")
    
    def test_extract_title_empty_string_input(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_placeholder(self):
        result = ""
        expectation = ""
        self.assertEqual(result, expectation)

if __name__ == "__main__":
    unittest.main()