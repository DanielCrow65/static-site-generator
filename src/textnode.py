from enum import Enum

class TextType(Enum):
    TEXT = 'Text'
    BOLD = 'Bold'
    ITALIC = 'Italic'
    CODE = 'Code'
    LINK = 'Link'
    IMAGE = 'Image'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # Compares 2 TextNode arguments if they have the same attributes
    def __eq__(self, second_node):
        if (
            self.text == second_node.text 
            and self.text_type == second_node.text_type
            and self.url == second_node.url):
            return True
        return False

    # Converts the TextNode argument's attributes into a single string
    def __repr__(self):
        str_text = str(self.text)
        str_text_type = self.text_type.value
        str_url = str(self.url)
        return f"TextNode({str_text}, {str_text_type}, {str_url})"