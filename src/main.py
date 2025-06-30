import os
import shutil
from conversion import markdown_to_html_node
from extraction import extract_title

def transfer_static_to_public(source, destination):
    # we call this outside of the recursive function because otherwise it will delete everything every recursion
    if os.path.exists(destination) is True: # shutil.rmtree raises an error if the destination does not exist, so catch it here
        shutil.rmtree(destination) # ensures that the destination is empty
    copy_directory(source, destination)

def copy_directory(source, destination):
    if not os.path.isdir(source): # first off, make sure source is a directory
        raise ValueError(f"Source path {source} must be a directory.")
    os.makedirs(destination, exist_ok=True) # This prevents errors being raised if the directory already exists
    source_list = os.listdir(source) # Get a list of files and directories inside the source path
    for item in source_list:
        path_to_check = os.path.join(source, item) # combine the source path with the item to get the full path for each item
        if os.path.isfile(path_to_check):
            shutil.copy(path_to_check, destination) # if the full path refers to a file, copy it over right away
            print(f"Copied {path_to_check} to {destination}") # log the instance of the files being copied
        else: # an invalid file name will be treated like a dir, no need to elif
            new_dir_path = os.path.join(destination, item) # do not use path_to_check here because it uses the source, we just need a relative path for this directory
            os.makedirs(new_dir_path, exist_ok=True)
            copy_directory(path_to_check, new_dir_path)
    return

# takes a markdown file stored in from_path, convert it an html file then insert it into the template, then put the final file in dest_path
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    # documentation says using with here cleanly lets me close the file after its done with the with block. 
    # I have to close the file manually if I don't use with (source_f.close())
    with open(from_path, encoding="utf-8") as source_f: 
        source_md = source_f.read() # this is a string
    with open(template_path, encoding="utf-8") as temp_f:
        template_html = temp_f.read() # this is also a string

    # grab the title from the source markdown
    # convert the source markdown into an html string ready for the webpage
    page_title = extract_title(source_md)
    webpage_content = markdown_to_html_node(source_md).to_html()

    # update the template with the content we extracted
    webpage_with_title = template_html.replace("{{ Title }}", page_title)
    complete_webpage = webpage_with_title.replace("{{ Content }}", webpage_content)

    # make sure the destination exists (specifically, the directory the destination path is on)
    # the following write file attempt will fail if we do not
    dest_dirname = os.path.dirname(dest_path) # this gets the directory the destination path is on, whether the last item is a dir or a file
    os.makedirs(dest_dirname, exist_ok=True)

    # write the complete_webpage into a file and then send it to the destination path
    # the dest_path ensures the file is created in the correct place
    with open(dest_path, mode="w", encoding="utf-8") as dest_f:
        dest_f.write(complete_webpage)

def generate_pages_recursive(dir_path_content, template_path, des_dir_path):
    lst_content_dir = os.listdir(dir_path_content) # get a list of all the files/directories in dir_path_content (./content must be here)
    for item in lst_content_dir:
        content_item_path = os.path.join(dir_path_content, item) # create the path to the current item being examined
        if os.path.isfile(content_item_path) and content_item_path.endswith(".md"):
            # This happens if a file is found and it is a markdown file
            new_html = item.replace(".md", ".html") # make sure the destination file is an html!
            new_des_path = os.path.join(des_dir_path, new_html) # to maintain the directory structure for the destination
            print(f"Found a markdown file at {content_item_path}! Generating a new page at {new_des_path}!") # DEBUG
            generate_page(content_item_path, template_path, new_des_path)
        elif os.path.isdir(content_item_path):
            # This happens if a directory is found
            new_des_path = os.path.join(des_dir_path, item) # to maintain the directory structure for the destination
            print(f"Found a new directory at {content_item_path}, looking inside...") # DEBUG
            generate_pages_recursive(content_item_path, template_path, new_des_path)
        else:
            # This happens if a file is found but it is not an md
            print(f"No markdown found at {content_item_path}, moving on...") # DEBUG
            pass
    print(f"All files successfully checked! Check out the new webpage at {des_dir_path}!") # DEBUG
        


def main():
    shutil.rmtree("./public", ignore_errors=True)
    transfer_static_to_public("./static", "./public") # this creates the directories if they do not already exist, revisit the functions if needed
    generate_pages_recursive("content", "template.html", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
main()