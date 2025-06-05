from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion import text_node_to_html_node

#print("hello world")

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            text_html = LeafNode(None, text_node.text, None)
            return text_html
        case TextType.BOLD:
            bold_html = LeafNode("b", text_node.text, None)
            return bold_html
        case TextType.ITALIC:
            italic_html = LeafNode("i", text_node.text, None)
            return italic_html
        case TextType.CODE:
            code_html = LeafNode("code", text_node.text, None)
            return code_html
        case TextType.LINK:
            link_html = LeafNode("a", text_node.text, {"href": text_node.url})
            return link_html
        case TextType.IMAGE:
            image_html = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return image_html
        case __:
            raise Exception("This text type is invalid")

def main():
    # TEXT NODE CHECK
    
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
    """

    #my_parentnode2 = ParentNode(None, my_list, None)
    #print(my_parentnode2.to_html())

    #my_parentnode3 = ParentNode("body", None, None)
    #print(my_parentnode3.to_html())

    #my_parentnode4 = ParentNode("body", [], None)
    #print(my_parentnode4.to_html())

    """
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.__repr__())
    print(parent_node.to_html())
    """

main()