from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from extraction import extract_markdown_images, extract_markdown_links
from markdown import BlockType, block_to_block_type

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_images = extract_markdown_images(node.text) # This gives me the list of tuples I need to make the Image TextNodes
            text_to_update = node.text
            if extracted_images != []: # If the list is empty, this TextNode has no image links in it
                for item in extracted_images:
                    image_alt = item[0] # grabs the alt text stored in the first index
                    image_link = item[1] # grabs the link string stored in the second index
                    # split the text using the markdown syntax as a delimiter, creating a list of ONLY 2 items
                    updated_text = text_to_update.split(f"![{image_alt}]({image_link})", 1) # this will ALWAYS produce 2 items
                    # grabs the first item and turns it into a normal textnode (normal text found before finding a link)
                    new_text_node = TextNode(updated_text[0], TextType.TEXT)
                    new_image_node = TextNode(image_alt, TextType.IMAGE, image_link)
                    if new_text_node.text.strip() != "": # skips adding to the final list if there is no text found, and disqualifies whitespace
                        new_nodes.extend([new_text_node])
                    if new_image_node.text.strip() != "":
                        new_nodes.extend([new_image_node])
                    text_to_update = updated_text[1] # prepares text_to_update for the next iteration of the loop
                # upon exiting the loop (gone through all of extracted_images), grab the remaining text and turn it into a TextNode!
                final_node = TextNode(text_to_update, TextType.TEXT)
                if final_node.text.strip() != "":
                    new_nodes.extend([final_node])
            else:
                new_nodes.extend([node]) # no image links were found so it is safe to extend the entire node
        else:
            new_nodes.extend([node])
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            extracted_links = extract_markdown_links(node.text)
            text_to_update = node.text
            if extracted_links != []:
                for item in extracted_links:
                    link_text = item[0]
                    link_href = item[1]
                    updated_text = text_to_update.split(f"[{link_text}]({link_href})", 1)
                    new_text_node = TextNode(updated_text[0], TextType.TEXT)
                    new_link_node = TextNode(link_text, TextType.LINK, link_href)
                    if new_text_node.text.strip() != "":
                        new_nodes.extend([new_text_node])
                    if new_link_node.text.strip() != "":
                        new_nodes.extend([new_link_node])
                    text_to_update = updated_text[1]
                final_node = TextNode(text_to_update, TextType.TEXT)
                if final_node.text.strip() != "":
                    new_nodes.extend([final_node])
            else:
                new_nodes.extend([node])
        else:
            new_nodes.extend([node])
    return new_nodes

def text_to_textnodes(text):
    # turn the inputted string into a normal TextNode first
    for_conversion = TextNode(text, TextType.TEXT)
    # split off links and images FIRST. They will NOT be processed if they were split off to non-TEXT TextNodes first
    new_text = split_nodes_image(split_nodes_link([for_conversion]))
    # since we do not support layered formatting, the order the text types are processed here does not matter
    new_text = split_nodes_delimiter(new_text, "**", TextType.BOLD)
    new_text = split_nodes_delimiter(new_text, "_", TextType.ITALIC)
    new_text = split_nodes_delimiter(new_text, "`", TextType.CODE)
    return new_text

def markdown_to_blocks(markdown):
    temp = markdown.split("\n\n")
    blocks_list = []
    for item in temp:
        new_item = item.strip()
        if new_item.strip() != "":
            blocks_list.append(new_item)
    return blocks_list

def text_to_children(text):
    # this helper function should take a string of text (inline markdown from a block) and return a LIST of HTMLNodes
    textnode_list = text_to_textnodes(text)
    htmlnode_list = [] # since text_to_textnodes returns a list, process them to html nodes and append them here
    for node in textnode_list:  
        new_htmlnode = text_node_to_html_node(node)
        htmlnode_list.append(new_htmlnode)
    return htmlnode_list

def markdown_to_html_node(markdown):
    # convert the text input into blocks
    raw_blocks = markdown_to_blocks(markdown)
    #print(raw_blocks)
    total_children = [] # append each completed htmlnode here, to be contained in a parent div node when all is said and done
    for block in raw_blocks:
        # determine type of block
        identified_block = block_to_block_type(block)

        # create new HTML node based on the block type
        if identified_block == BlockType.HEAD:
            # identify how many # characters we have to prepare to slice off later
            header_count = 0
            for char in block:
                if char == "#":
                    header_count += 1
                else:
                    # exit the loop upon encountering a non # character (should be the whitespace)
                    break # Boots tels me this is not in fact a bad habit and break is perfectly fine to use
            match header_count:
                case 1:
                    new_tag = "h1" 
                case 2:
                    new_tag = "h2"
                case 3:
                    new_tag = "h3"
                case 4:
                    new_tag = "h4"
                case 5:
                    new_tag = "h5"
                case 6:
                    new_tag = "h6"
            edited_block = block[header_count + 1:] # this should slice the text, excluding the unneeded markdown tags
            processed_block = edited_block.replace("\n", " ") # my function will treat a header block with a newline as a single block, so I need to get rid of any internal newlines
            inline_markdown = text_to_children(processed_block)
            new_node = ParentNode(new_tag, inline_markdown, None)
            total_children.append(new_node)
            
        elif identified_block == BlockType.PARA:
            processed_block = block.replace("\n", " ") # newlines must be replaced with whitespace, for that's how browsers handle paragraph blocks
            inline_markdown = text_to_children(processed_block)
            new_node = ParentNode("p", inline_markdown, None)
            total_children.append(new_node)

        elif identified_block == BlockType.QUOT:
            processed_block = block.split("\n") # we have to get rid of the > markdown syntax for each line in the block
            list_for_join = [] # ...and we also need to put the string back together afterwards
            for line in processed_block:
                new_line = line.lstrip("> ")
                list_for_join.append(new_line)
            edited_block = "\n".join(list_for_join) # remember, we need a single string for text_to_children, not a list!
            
            inline_markdown = text_to_children(edited_block)
            new_node = ParentNode("blockquote", inline_markdown, None)
            total_children.append(new_node)
        
        elif identified_block == BlockType.CODE:
            processed_block = block.strip("```").lstrip() # this should catch the ``` at the start and at the end of the block. The 2nd strip should take care of whitespace
            code_textnode = TextNode(processed_block, TextType.CODE)
            child_code_node = [text_node_to_html_node(code_textnode)] # though it is just a single item, the children property must be a list
            new_node = ParentNode("pre", child_code_node, None) # pre tag is for block level code. Inline code is just wrapped in code
            total_children.append(new_node)
        
        elif identified_block == BlockType.ULIST:
            processed_block = block.split("\n")
            list_item_nodes = []
            for line in processed_block:
                new_line = line.lstrip("- ").lstrip("* ") # removed unwanted markdown syntax
                processed_line = text_to_children(new_line)
                new_list_item = ParentNode("li", processed_line, None) # since each list item has its own tag, process to HTML node now
                list_item_nodes.append(new_list_item)
            new_node = ParentNode("ul", list_item_nodes, None) # each child was already processed into a list
            total_children.append(new_node)

        elif identified_block == BlockType.OLIST:
            processed_block = block.split("\n")
            list_item_nodes = []
            for line in processed_block:
                for_slice_index = line.find(".") # since the index of each item in the list changes dynamically, ignore it altogether...
                new_line = line[for_slice_index + 1:].lstrip() # ...by finding the period and then slicing away the rest of the list
                # +1 is to get the proper index to slice off of (the index after the period) 
                # and lstrip will flexibly remove any number of whitespace after the period
                processed_line = text_to_children(new_line)
                new_list_item = ParentNode("li", processed_line, None)
                list_item_nodes.append(new_list_item)
            new_node = ParentNode("ol", list_item_nodes, None)
            total_children.append(new_node)
    
    div_node = ParentNode("div", total_children, None)
    return div_node

""" NOTES """
# Paragraph blocks are interpreted as a single line. So newlines, or tabs will be processed into a single whitespace to maintain
# single line interpretation
#