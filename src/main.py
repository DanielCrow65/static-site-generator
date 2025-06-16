from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion import split_nodes_delimiter
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
    # TEXT NODE CHECK
    """
    my_textnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    my_textnode2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    my_textnode3 = TextNode("This is another example of anchor text", TextType.LINK, "https://www.boot.dev")
    print(my_textnode.__repr__())
    print(my_textnode.__eq__(my_textnode2))
    print(my_textnode.__eq__(my_textnode3))
    
    my_textnode_text = TextNode("I am just raw text", TextType.TEXT)
    print(my_textnode_text.__repr__())
    my_new_html_node1 = text_node_to_html_node(my_textnode_text)
    print(my_new_html_node1)

    my_textnode_italic = TextNode("I feel a bit tilted", TextType.ITALIC)
    print(my_textnode_italic.__repr__())
    my_new_html_node2 = text_node_to_html_node(my_textnode_italic)
    print(my_new_html_node2)

    my_textnode_bold = TextNode("I am feeling bold at the moment", TextType.BOLD)
    print(my_textnode_bold.__repr__())
    my_new_html_node3 = text_node_to_html_node(my_textnode_bold)
    print(my_new_html_node3)
    
    my_textnode_code = TextNode("I am a block of code", TextType.CODE)
    print(my_textnode_code.__repr__())
    my_new_html_node4 = text_node_to_html_node(my_textnode_code)
    print(my_new_html_node4)
    
    my_textnode_link = TextNode("Test Link", TextType.LINK, "www.wikipedia.org")
    print(my_textnode_link.__repr__())
    my_new_html_node5 = text_node_to_html_node(my_textnode_link)
    print(my_new_html_node5)

    my_textnode_image = TextNode("Test Image", TextType.IMAGE, "/images/assets/sample.png")
    print(my_textnode_image.__repr__())
    my_new_html_node6 = text_node_to_html_node(my_textnode_image)
    print(my_new_html_node6)
    """
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

    # PARENT NODE CHECK
    """
    child_one = LeafNode("h2","Test Heading")
    child_two = LeafNode('a', "Test line here", {"href": "www.google.com", "target": "_blank"})
    my_list = [child_one, child_two]
    my_parentnode = ParentNode("body", my_list, None)
    print(my_parentnode.__repr__())
    print(my_parentnode.to_html())

    my_parentnode2 = ParentNode(None, my_list, None)
    print(my_parentnode2.to_html())

    my_parentnode3 = ParentNode("body", None, None)
    print(my_parentnode3.to_html())

    my_parentnode4 = ParentNode("body", [], None)
    print(my_parentnode4.to_html())
    
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.__repr__())
    print(parent_node.to_html())
    """

    #SPLIT NODES TESTS
    """
    node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
    result_basic_input = split_nodes_delimiter([node1], "`", TextType.CODE)
    print(result_basic_input)

    node2 = TextNode("`I start with a delimiter`, hope you can handle me.", TextType.TEXT)
    result_delimited_start = split_nodes_delimiter([node2], "`", TextType.CODE)
    print(result_delimited_start)

    node3 = TextNode("I have `multiple` delimited `segments` so I hope you got this", TextType.TEXT)
    result_multiple_delimited = split_nodes_delimiter([node3], "`", TextType.CODE)
    print(result_multiple_delimited)    

    node4 = TextNode("I end in a `code block`", TextType.TEXT)
    result_delimited_end = split_nodes_delimiter([node4], "`", TextType.CODE)
    print(result_delimited_end)

    node5 = TextNode("**I start with a delimiter** and I have **another delimiter at the end**", TextType.TEXT)
    result_delimited_start_and_end = split_nodes_delimiter([node5], "**", TextType.BOLD)
    print(result_delimited_start_and_end)

    node6 = TextNode("I am a perfectly normal set of raw text", TextType.TEXT)
    result_multichar_delimiter = split_nodes_delimiter([node6], "**", TextType.BOLD)
    print (result_multichar_delimiter)

    node7 = TextNode("I am just raw text!", TextType.TEXT)
    node8 = TextNode("I am a piece of italic text!", TextType.ITALIC)
    node9 = TextNode("I am another set of raw text!", TextType.TEXT)
    result_multiple_node_input = split_nodes_delimiter([node7, node8, node9], "_", TextType.ITALIC)
    print(result_multiple_node_input)
    """

    # REGEX TESTS
    # Basic Regex test
    text = "I'm a little teapot, short and stout. Here is my handle, here is my spout."
    matches = re.findall(r"teapot", text)
    print(matches) # ['teapot']

    text = "My email is lane@example.com and my friend's email is hunter@example.com"
    matches = re.findall(r"(\w+)@(\w+\.\w+)", text)
    print(matches)  # [('lane', 'example.com'), ('hunter', 'example.com')]
    
    # Extract markdown image
    text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    print(extract_markdown_images(text)) 
    # [('image', 'https://i.imgur.com/zjjcJKZ.png')]

    # Extract markdown link
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

main()