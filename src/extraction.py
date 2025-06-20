import re

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