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
    os.makedirs(destination, exist_ok=True)
    source_list = os.listdir(source)
    for item in source_list:
        path_to_check = os.path.join(source, item)
        if os.path.isfile(path_to_check):
            shutil.copy(path_to_check, destination)
            print(f"Copied {path_to_check} to {destination}") # log the instance of the files being copied
        else: # an invalid file name will be treated like a dir, no need to elif)
            new_directory = os.path.join(destination, item) # do not use path_to_check here because it uses the source, we just need a relative path for this directory
            os.makedirs(new_directory, exist_ok=True)
            copy_directory(path_to_check, new_directory)
    return

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


def main():
    shutil.rmtree("./public", ignore_errors=True)
    transfer_static_to_public("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()