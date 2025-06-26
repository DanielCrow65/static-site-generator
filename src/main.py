from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from markdown import block_to_block_type
import re

#print("hello world")

def extract_markdown_images(text):
    # Accept text string
    # Extract markdown syntax for image
    # Return list of tuples, each tuple containing the alt text and markdown lists (both in the url property of a image type text node)
    image_match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) # this creates a list 
    return image_match

def extract_markdown_links(text):
    # Accept text string
    # Extract markdown syntax for image
    # Return list of tuples, each tuple containing anchor text and the href (text property and url property of a link type text node)
    link_match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_match

def main():
    # These rough tests are converted into proper unit tests in the test module
    """ TEXT NODE CHECK """
    # my_textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # my_textnode2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # my_textnode3 = TextNode("This is another example of anchor text", TextType.LINK, "https://www.boot.dev")
    # print(my_textnode.__repr__())
    # print(my_textnode.__eq__(my_textnode2))
    # print(my_textnode.__eq__(my_textnode3))
    
    # my_textnode_text = TextNode("I am just raw text", TextType.TEXT)
    # print(my_textnode_text.__repr__())
    # my_new_html_node1 = text_node_to_html_node(my_textnode_text)
    # print(my_new_html_node1)

    # my_textnode_italic = TextNode("I feel a bit tilted", TextType.ITALIC)
    # print(my_textnode_italic.__repr__())
    # my_new_html_node2 = text_node_to_html_node(my_textnode_italic)
    # print(my_new_html_node2)

    # my_textnode_bold = TextNode("I am feeling bold at the moment", TextType.BOLD)
    # print(my_textnode_bold.__repr__())
    # my_new_html_node3 = text_node_to_html_node(my_textnode_bold)
    # print(my_new_html_node3)
    
    # my_textnode_code = TextNode("I am a block of code", TextType.CODE)
    # print(my_textnode_code.__repr__())
    # my_new_html_node4 = text_node_to_html_node(my_textnode_code)
    # print(my_new_html_node4)
    
    # my_textnode_link = TextNode("Test Link", TextType.LINK, "www.wikipedia.org")
    # print(my_textnode_link.__repr__())
    # my_new_html_node5 = text_node_to_html_node(my_textnode_link)
    # print(my_new_html_node5)

    # my_textnode_image = TextNode("Test Image", TextType.IMAGE, "/images/assets/sample.png")
    # print(my_textnode_image.__repr__())
    # my_new_html_node6 = text_node_to_html_node(my_textnode_image)
    # print(my_new_html_node6)

    # HTML NODE CHECK WITH PROPS
    """
    my_htmlnode = HTMLNode('a', "Test line here", None, {"href": "www.google.com", "target": "_blank"})
    print(my_htmlnode.__repr__())
    """
    
    # HTML NODE CHECK WITH CHILDREN
    """
    child_one = HTMLNode("h2","Test Heading")
    child_two = HTMLNode("p", "Test Paragraph")
    my_list = [child_one, child_two]

    my_htmlnode_2 = HTMLNode("h1", None, my_list)
    print(my_htmlnode_2.__repr__())
    """

    # LEAF NODE CHECK
    """
    my_leafnode = LeafNode("a", "Click!", {"href": "www.google.com", "target": "_blank"})
    print(my_leafnode.__repr__())
    """

    """ PARENT NODE CHECK """
    # child_one = LeafNode("h2","Test Heading")
    # child_two = LeafNode('a', "Test line here", {"href": "www.google.com", "target": "_blank"})
    # my_list = [child_one, child_two]
    # my_parentnode = ParentNode("body", my_list, None)
    # print(my_parentnode.__repr__())
    # print(my_parentnode.to_html())

    # my_parentnode2 = ParentNode(None, my_list, None)
    # print(my_parentnode2.to_html())

    # my_parentnode3 = ParentNode("body", None, None)
    # print(my_parentnode3.to_html())

    # my_parentnode4 = ParentNode("body", [], None)
    # print(my_parentnode4.to_html())
    
    # grandchild_node = LeafNode("b", "grandchild")
    # child_node = ParentNode("span", [grandchild_node])
    # parent_node = ParentNode("div", [child_node])
    # print(parent_node.__repr__())
    # print(parent_node.to_html())

    """ SPLIT NODES TESTS """
    # node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
    # result_basic_input = split_nodes_delimiter([node1], "`", TextType.CODE)
    # print(result_basic_input)

    # node2 = TextNode("`I start with a delimiter`, hope you can handle me.", TextType.TEXT)
    # result_delimited_start = split_nodes_delimiter([node2], "`", TextType.CODE)
    # print(result_delimited_start)

    # node3 = TextNode("I have `multiple` delimited `segments` so I hope you got this", TextType.TEXT)
    # result_multiple_delimited = split_nodes_delimiter([node3], "`", TextType.CODE)
    # print(result_multiple_delimited)    

    # node4 = TextNode("I end in a `code block`", TextType.TEXT)
    # result_delimited_end = split_nodes_delimiter([node4], "`", TextType.CODE)
    # print(result_delimited_end)

    # node5 = TextNode("**I start with a delimiter** and I have **another delimiter at the end**", TextType.TEXT)
    # result_delimited_start_and_end = split_nodes_delimiter([node5], "**", TextType.BOLD)
    # print(result_delimited_start_and_end)

    # node6 = TextNode("I am a perfectly normal set of raw text", TextType.TEXT)
    # result_multichar_delimiter = split_nodes_delimiter([node6], "**", TextType.BOLD)
    # print (result_multichar_delimiter)

    # node7 = TextNode("I am just raw text!", TextType.TEXT)
    # node8 = TextNode("I am a piece of italic text!", TextType.ITALIC)
    # node9 = TextNode("I am another set of raw text!", TextType.TEXT)
    # result_multiple_node_input = split_nodes_delimiter([node7, node8, node9], "_", TextType.ITALIC)
    # print(result_multiple_node_input)

    """ REGEX TESTS """
    # Basic Regex test
    # text = "I'm a little teapot, short and stout. Here is my handle, here is my spout."
    # matches = re.findall(r"teapot", text)
    # print(matches) # ['teapot']

    # text = "My email is lane@example.com and my friend's email is hunter@example.com"
    # matches = re.findall(r"(\w+)@(\w+\.\w+)", text)
    # print(matches)  # [('lane', 'example.com'), ('hunter', 'example.com')]
    
    # Extract markdown image
    # text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    # print(extract_markdown_images(text)) 
    # # [('image', 'https://i.imgur.com/zjjcJKZ.png')]

    # # Extract markdown link
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))
    # # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    # Extract markdown image with no alt text
    # text = "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
    # print(extract_markdown_images(text)) 
    # [('', 'https://i.imgur.com/zjjcJKZ.png')]

    """ SPLIT IMAGE TESTS """
    # node = TextNode(
    #         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    #         TextType.TEXT,
    #     )
    # print(split_nodes_image([node]))
    # # [TextNode(This is text with an , Text, None), TextNode(image, Image, https://i.imgur.com/zjjcJKZ.png), 
    # # TextNode( and another , Text, None), TextNode(second image, Image, https://i.imgur.com/3elNhQu.png)]

    # text_node_with_no_images = TextNode("I am a simple text node with no images!", TextType.TEXT)
    # print(split_nodes_image([text_node_with_no_images]))
    # # [TextNode(I am a simple text node with no images!, Text, None)]

    # non_text_node = TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD)
    # print(split_nodes_image([non_text_node]))
    # # [TextNode(**I am not a simple text node, but not an image node either!**, Bold, None)]

    # # Test for image markdowns right next to each other
    # text_node_adjacent_images = TextNode("I have ![two](https://i.imgur.com/zjjcJKZ.png) ![images](https://i.imgur.com/3elNhQu.png) next to each other!", TextType.TEXT)
    # print(split_nodes_image([text_node_adjacent_images]))
    # # [TextNode(I have , Text, None), TextNode(two, Image, https://i.imgur.com/zjjcJKZ.png), TextNode(images, Image, https://i.imgur.com/3elNhQu.png), TextNode( next to each other!, Text, None)]

    # text_node_truly_adjacent_images = TextNode("I have ![two](https://i.imgur.com/zjjcJKZ.png)![images](https://i.imgur.com/3elNhQu.png) next to each other! And no whitespace!", TextType.TEXT)
    # print(split_nodes_image([text_node_truly_adjacent_images]))
    # # [TextNode(I have , Text, None), TextNode(two, Image, https://i.imgur.com/zjjcJKZ.png), TextNode(images, Image, https://i.imgur.com/3elNhQu.png), TextNode( next to each other! And no whitespace!, Text, None)]

    # # Test of image markdowns a the very beginning and end
    # text_node_image_start = TextNode("![I start with an image](https://i.imgur.com/zjjcJKZ.png), I hope that isn't an issue.", TextType.TEXT)
    # text_node_image_end = TextNode("Hopefully no problems that I end with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
    # print(split_nodes_image([text_node_image_start]))
    # # [TextNode(I start with an image, Image, https://i.imgur.com/zjjcJKZ.png), TextNode(, I hope that isn't an issue., Text, None)]
    # print(split_nodes_image([text_node_image_end]))
    # # [TextNode(Hopefully no problems that I end with an , Text, None), TextNode(image, Image, https://i.imgur.com/zjjcJKZ.png)]

    # non_text_nodes_multiple = [
    #     TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD), 
    #     TextNode("_And I am also here!_", TextType.ITALIC)]
    # print(split_nodes_image(non_text_nodes_multiple))
    # # [TextNode(**I am not a simple text node, but not an image node either!**, Bold, None), 
    # # TextNode(_And I am also here!_, Italic, None)]

    # text_nodes_multiple = [
    #     TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT), 
    #     TextNode("**I am not a simple text node, but not an image node either!**", TextType.BOLD),
    #     TextNode("I am a simple text node with no images!", TextType.TEXT)]
    # print(split_nodes_image(text_nodes_multiple))
    # # [TextNode(This is text with an , Text, None), TextNode(image, Image, https://i.imgur.com/zjjcJKZ.png), TextNode(**I am not a simple text node, but not an image node either!**, Bold, None), TextNode(I am a simple text node with no images!, Text, None)]

    # text_node_start_and_end = TextNode("![I start with an image](https://i.imgur.com/zjjcJKZ.png) and I end with ![one too.](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
    # print(split_nodes_image([text_node_start_and_end]))

    """ SPLIT LINK TESTS """
    # # Happy Path with multiple inputs (and ends on a link)
    # link_node_test = TextNode(
    #     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
    #     TextType.TEXT)
    # print(split_nodes_link([link_node_test]))
    # # [TextNode(This is text with a link , Text, None), TextNode(to boot dev, Link, https://www.boot.dev), 
    # # TextNode( and , Text, None), TextNode(to youtube, Link, https://www.youtube.com/@bootdotdev)]

    # # Just a TextNode with no links
    # text_node_with_no_links = TextNode("I am a simple text node with no links!", TextType.TEXT)
    # print(split_nodes_link([text_node_with_no_links]))
    # # [TextNode(I am a simple text node with no links!, Text, None)]

    # # A non-TEXT TextNode (with a link that should be ignored)
    # non_text_node = TextNode("**I am not a simple text node, but I am not a [link node](https://www.boot.dev), either!", TextType.BOLD)
    # print(split_nodes_link([non_text_node]))
    # # [TextNode(**I am not a simple text node, but I am not a [link node](https://www.boot.dev), either!, Bold, None)]

    # # Link at the start of the string
    # link_node_start = TextNode("[Boot dev](https://www.boot.dev) is an excellent website!", TextType.TEXT)
    # print(split_nodes_link([link_node_start]))
    # # [TextNode(Boot dev, Link, https://www.boot.dev), TextNode( is an excellent website!, Text, None)]

    # # Adjacent markdown links
    # link_node_adjacent = TextNode("I have [two](https://www.boot.dev)[links](https://www.youtube.com/@bootdotdev) right next to each other.", TextType.TEXT)
    # print(split_nodes_link([link_node_adjacent]))
    # # [TextNode(I have , Text, None), TextNode(two, Link, https://www.boot.dev), 
    # # TextNode(links, Link, https://www.youtube.com/@bootdotdev), TextNode( right next to each other., Text, None)]

    # # Link separated with whitespace
    # link_node_whitespace = TextNode("I have [two](https://www.boot.dev) [links](https://www.youtube.com/@bootdotdev) on me too!", TextType.TEXT)
    # print(split_nodes_link([link_node_whitespace]))
    # # [TextNode(I have , Text, None), TextNode(two, Link, https://www.boot.dev), 
    # # TextNode(links, Link, https://www.youtube.com/@bootdotdev), TextNode( on me too!, Text, None)]

    # # Multiple nodes with no links
    # non_text_nodes_multiple = [
    #         TextNode("**I am not a simple text node, but not a link node either!**", TextType.BOLD), 
    #         TextNode("_And I am also here!_", TextType.ITALIC)]
    # print(split_nodes_link(non_text_nodes_multiple))
    # # [TextNode(**I am not a simple text node, but not a link node either!**, Bold, None), 
    # # TextNode(_And I am also here!_, Italic, None)]

    # # Multiple nodes with some links
    # text_nodes_multiple = [
    #         TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT), 
    #         TextNode("**I am not a simple text node, but not a link node either!**", TextType.BOLD),
    #         TextNode("I am a simple text node with no links!", TextType.TEXT)]
    # print(split_nodes_link(text_nodes_multiple))
    # # [TextNode(This is text with a , Text, None), TextNode(link, Link, https://www.boot.dev), 
    # # TextNode(**I am not a simple text node, but not a link node either!**, Bold, None), 
    # # TextNode(I am a simple text node with no links!, Text, None)]

    """ TEXT TO TEXTNODE TESTS """
    # my_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # print(text_to_textnodes(my_text))
    # # [TextNode(This is , Text, None), TextNode(text, Bold, None), TextNode( with an , Text, None), 
    # # TextNode(italic, Italic, None), TextNode( word and a , Text, None), TextNode(code block, Code, None), 
    # # TextNode( and an , Text, None), TextNode(obi wan image, Image, https://i.imgur.com/fJRm4Vk.jpeg), 
    # # TextNode( and a , Text, None), TextNode(link, Link, https://boot.dev)]

    # layered_text = "I have **_a bolded italic word_** in me..."
    # print(text_to_textnodes(layered_text))
    # # [TextNode(I have , Text, None), TextNode(_a bolded italic word_, Bold, None), TextNode( in me..., Text, None)]

    # adjacent_delim_text = "_I happen_ **to have** `adjacent delimiters` and really **adjacent**_ones_`too`"
    # print(text_to_textnodes(adjacent_delim_text))
    # # [TextNode(I happen, Italic, None), TextNode( , Text, None), TextNode(to have, Bold, None), 
    # # TextNode( , Text, None), TextNode(adjacent delimiters, Code, None), TextNode( and really , Text, None), 
    # # TextNode(adjacent, Bold, None), TextNode(ones, Italic, None), TextNode(too, Code, None)]

    """ MARKDOWN TO BLOCKS TEST """
#     # happy path
#     md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items
# """
#     print(markdown_to_blocks(md))
#     # ['This is **bolded** paragraph', 'This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line', '- This is a list\n- with items']

#     # empty block to eliminate
#     excess = """
# My paragraph is quite nice.



# But there might be
# some extra space that does not belong there?

# How vexing.
# """

#     print(markdown_to_blocks(excess))
#     # ['My paragraph is quite nice.', 'But there might be\nsome extra space that does not belong there?', 'How vexing.']

#     # begins or ends with empty blank lines/white space
#     start_and_end = """


# I have an empty line before me.

# I have a two white spaces behind me.
 
 
# """
#     print(markdown_to_blocks(start_and_end))
#     # ['I have an empty line before me.', 'I have a two white spaces behind me.']

#     # markdown has no blank spaces
#     no_blank = """
# I have some strings, to pull me down
# but I got no blank spaces on me
# Just a continuous stream
# of issue.
# """
#     print(markdown_to_blocks(no_blank))
#     # ['I have some strings, to pull me down\nbut I got no blank spaces on me\nJust a continuous stream\nof issue.']

#     # just an empty string
#     print(markdown_to_blocks(""))
#     # []

#     # only whitespace (spaces, tabs, newlines)
#     only_whitespace = """


 
 

    

# """
#     print(markdown_to_blocks(only_whitespace))
#     # []

#     md = """
# - I am a list
# - I have no order
# - Let chaos reign!
# """
#     result = block_to_block_type(md)
#     print(result)

#     md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """

#     node = markdown_to_html_node(md)
#     print(node.to_html())
#     # print(node)

#     md2 = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
#     node2 = markdown_to_html_node(md2)
#     print(node2.to_html())

#     md3 = """
# # I am a header block

# ## And so am I!

# ### Me too!

# #### Don't forget about me!

# ##### I'm not late to the party, am I?

# ###### Hey wait for me!
# """
#     node3 = markdown_to_html_node(md3)
#     print(node3.to_html())

#     md4 = """
# # Welcome

# This is a paragraph.

# * List item one
# * List item two

# > This is a quote.

# ```
# some_code = "hello"
# ```

# ## Subheading

# Another paragraph here.
# """
#     node4 = markdown_to_html_node(md4)
#     print(node4.to_html())
#     # <div><h1>Welcome</h1><p>This is a paragraph.</p><ul><li>List item one</li><li>List item two</li></ul><blockquote>This is a quote.</blockquote><pre><code>some_code = \"hello\"\n</code></pre><h2>Subheading</h2><p>Another paragraph here.</p></div>
main()