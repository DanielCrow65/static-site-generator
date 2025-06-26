from enum import Enum

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOT = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(text):
    if text.startswith("#"): # HEADING
        if text.startswith("# "):
            return BlockType.HEAD
        elif text.startswith("## "):
            return BlockType.HEAD
        elif text.startswith("### "):
            return BlockType.HEAD
        elif text.startswith("#### "):
            return BlockType.HEAD
        elif text.startswith("##### "):
            return BlockType.HEAD
        elif text.startswith("###### "):
            return BlockType.HEAD

        """ Shorter option offered by Boots """
        # valid_headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
        # if any(text.startswith(heading) for heading in valid_headings):
        #     return BlockType.HEAD
    
    # CODE
    elif text.startswith("```"): 
        if text.endswith("```"):
            return BlockType.CODE
        return BlockType.PARA
    
    # QUOTE
    elif text.startswith(">"): 
        temp = text.split("\n") # Check if the rest of the block is also quoted
        for item in temp:
            if item.startswith(">") is False:
                return BlockType.PARA # if the syntax is ever not met correctly, just treat it like a normal block
        return BlockType.QUOT # If the loop exits safely without triggering False, I can assume it is a complete Quote block
            
    # UNORDERED LIST
    # both - and * are acceptable markdown syntax for unordered lists
    elif text.startswith("- ") or text.startswith("* "):
        temp = text.split("\n")
        for item in temp:
            if not item.startswith("- ") and not item.startswith("* "):
                return BlockType.PARA
        return BlockType.ULIST
                
    # ORDERED LIST
    else:
        first_line = text.split("\n")[0] # split the text but only check the first line for now
        first_period_index = first_line.find(".") # find the period in the first line in the split text input
        # if no period is found, the first_line is not a proper list item
        # check if there is a valid number before the period
        # check if there is a whitespace directly after the period (and there is actually more after that space)
        # i.e. '1. ' with nothing after it is not a valid list item
        if first_period_index != -1 and \
            first_line[:first_period_index].isdigit() and \
            (first_period_index + 1 < len(first_line) and first_line[first_period_index + 1] == ' '):
            temp = text.split("\n") # if first_line passed all checks, then validate the rest of the text
            for item in temp:
                period_index = item.find(".")
                if period_index == -1:
                    return BlockType.PARA
                if not item[:period_index].isdigit():
                    return BlockType.PARA
                if not (period_index + 1 < len(item) and item[period_index + 1] == ' '):
                    return BlockType.PARA
            return BlockType.OLIST # If all lines passed, it's an ordered list
        else:
            return BlockType.PARA
    return BlockType.PARA