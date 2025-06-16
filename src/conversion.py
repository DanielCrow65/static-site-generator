from textnode import TextType, TextNode
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    #text_list = [] # This was used to test the string inputs
    #delimited_list = [] # This was used to test the string inputs
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            node_text = node.text
            #print(node_text)
            del_index = node_text.find(delimiter) # Find the index of the delimiter (this is the first delimiter)
            if del_index == 0: # This happens if the string already begins with a delimiter
                within_delimiter = True
            else:
                within_delimiter = False

            while node_text != "":
                if within_delimiter is False:
                    del_index = node_text.find(delimiter) # find the delimiter at the current iteration of node_text (should get shorter over time)
                    if del_index == -1:
                        temp = node_text # did not find another delimiter, so grab the remainder of node_text
                        text_node = TextNode(temp, TextType.TEXT)
                        node_text = "" # we can safely mark node_text as an empty string to end the loop because temp stores the original value
                    else:
                        temp = node_text[:del_index] # This grabs the string up to but not including the delimiter
                        text_node = TextNode(temp, TextType.TEXT)
                    #text_list.append(temp) This was used to test the string inputs. Not needed for directly using TextNodes
                    new_nodes.append(text_node)
                    node_text = node_text[del_index:] # after getting everything up to the delimiter, we re-calculate node_text after the delimiter
                    #print(node_text)
                    within_delimiter = True
                elif within_delimiter is True:
                    close_del_index = node_text[1:].find(delimiter) # Exclude index 0 (where the first delimiter is) and find the second one
                    if close_del_index == -1:
                        # currently in a delimited string but the string ended before finding the closing delimiter
                        raise ValueError("No closing delimiter for the last node")
                    else:
                        close_del_index += 1 # This is to get the correct index for slicing
                        temp = node_text[len(delimiter):close_del_index] # len(delimiter) accounts for delimiters that are more than 1 character
                        delimited_node = TextNode(temp, text_type)
                    #delimited_list.append(temp) This was used to test the string inputs. Not needed for directly using TextNodes
                    new_nodes.append(delimited_node)
                    node_text = node_text[close_del_index + len(delimiter):] # len(delimiter) accounts for delimiters that are more than 1 character
                    #print(node_text)
                    within_delimiter = False

            # These check if the lists are correct upon exiting the loop
            #print(node_text)
            #print(text_list)
            #print(delimited_list)
            #print(new_nodes)
        else:
            new_nodes.extend([node]) # If the text node presented was not a TEXT text type, it does not need to be split
    return new_nodes