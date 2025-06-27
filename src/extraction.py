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

# Extracts the first h1 tag encountered from a markdown input (markdown preceded with a single #)
def extract_title(markdown):
    md_for_inspection = markdown.split("\n") # it does not matter where the title is in the input, we just have to find it *somewhere*
    for line in md_for_inspection:
        if line.startswith("# "):
            title = line[2:].lstrip()
            if title == "":
                raise Exception("Your title is empty!")
            return title
    raise Exception("Markdown input has no header.")