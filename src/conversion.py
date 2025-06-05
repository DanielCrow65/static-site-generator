from textnode import TextType
from htmlnode import LeafNode

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