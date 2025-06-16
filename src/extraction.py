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