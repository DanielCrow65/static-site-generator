
class HTMLNode:
    # tag - for HTML tags like <head> and <p>. If None, it is just raw text
    # value - for the body of text enclosed within the tags. If None, assume there are children
    # children - a list of HTMLNode object representing the children of this node. If None, assume there is a value
    # props - a dict representing the attributes of the HTML tag (like href for the 'a' tag). Attributes are optional
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    # child classes will override this
    def to_html(self):
        raise NotImplementedError
    
    # takes the props (a dict) and convert it into a single string (with spaces between each entry)
    # the purpose of this method is to return an HTML-friendly string format, so it should always return a string
    def props_to_html(self):
        final_string = ""
        if self.props is None or self.props == "" or self.props == {}:
            return final_string
        for key, value in self.props.items():
            final_string += f" {key}=\"{value}\""
        return final_string

    def __repr__(self):
        str_tag = str(self.tag)
        str_value = str(self.value)
        if self.children is None:
            str_children = None
        else:
            temp_list = []
            for child in self.children:
                temp_list.append(child.__repr__())
            str_children = "\n".join(temp_list)
        str_props = self.props_to_html()
        return f"HTMLNode: {str_tag}, {str_value}, {str_children}, {str_props}"

# An HTML Node with no children. Like the 'leaves' coming out of an HTML tree
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        # to_html also does a check but checking here prevents a bad node from being created to begin with
        if value is None:
            raise ValueError("leaf node must have value")
        # Since there must be no children, and it is not the last argument
        # We have to use keyword arguments for all constructor tags
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have value")
        
        open_tag = ""
        close_tag = ""
        if self.tag is None or self.tag == "":
            pass
        else:
            open_tag = f"<{self.tag}{self.props_to_html()}>"
            close_tag = f"</{self.tag}>"
        return f"{open_tag}{self.value}{close_tag}"

# An HTML Node with children. Any node not a leaf is a parent    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        #if tag is None or children is None:
        #    raise ValueError("parent must have tag or children")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent must have tag")
        if self.children is None:
            raise ValueError("parent must have children")
        
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return f"{open_tag}{children_string}{close_tag}"