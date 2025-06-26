import os
import shutil

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

def main():
    transfer_static_to_public("./static", "./public")

    # EMPTY SOURCE TEST
    # empty_directory = "./static/empty"
    # to_be_emptied = "./public/empty"
    # print(os.listdir(empty_directory)) # []
    # print(os.listdir(to_be_emptied)) # ['useless-stuff.md', 'bad-styles.css', 'fake-emails.md']

    # transfer_static_to_public(empty_directory, to_be_emptied)

    # print(os.listdir(empty_directory)) # []
    # print(os.listdir(to_be_emptied)) # []

    # NON-EXISTENT DESTINATION TEST
    # full_source = "./static/test" 
    # shallow_destination = "./public/trash" # differently named directory here and does not exist yet
    # print(os.listdir(full_source))

    # transfer_static_to_public(full_source, shallow_destination)

    # print(os.listdir(full_source))
    # print(os.listdir(shallow_destination))

    # source = "./static/index.css"
    # destination = "./public/test/index.css"

    # test = shutil.copy(source, destination)
    # print(test)

    # path1 = "./static/index.css" # file that already exists
    # path2 = "./public/test/test.md" # file that does not exist
    # path3 = "./public/misc" # directory that does not exist
    
    # print(os.path.exists(path1)) # True
    # print(os.path.exists(path2)) # False
    # print(os.path.exists(path3)) # False

    # print(os.path.isfile(path1)) # True
    # print(os.path.isfile(path2)) # False
    # print(os.path.isfile(path3)) # False

    # # os.listdir testing
    # current_directory = "."
    # src_directory = "./src"
    # print(os.listdir(current_directory)) # ['main.sh', 'src', 'public', '.git', '.gitignore', 'test.sh', 'static']
    # print(os.listdir(src_directory)) # ['__pycache__', 'markdown.py', 'conversion.py', 'htmlnode.py', 'extraction.py', 'textnode.py', 'main.py', 'test.py']
    
    # # os.path.join testing
    # custom_path = os.path.join(".", "src") # this command automatically adds / between arguments, and only accepts strings
    # print(custom_path) # ./src
    # print(os.listdir(custom_path)) # ['__pycache__', 'markdown.py', 'conversion.py', 'htmlnode.py', 'extraction.py', 'textnode.py', 'main.py', 'test.py']

    # Try to create a custom path, make a directory, make a file then check if it exists
    # mkdir will fail if the directory already exists
    # new_path = os.path.join(".", "public", "test")
    # os.mkdir(new_path + "/special") # try to create a new directory called special inside test
    # new_file = shutil.copy("./static/index.css", new_path + "/special")
    # print(os.path.exists(new_file)) # True

    # os.makedirs testing
    # newer_path = os.path.join(".", "special", "awesome", "dir")
    # os.makedirs(newer_path, exist_ok=True) # setting exist_ok to True prevents error raising if the directory already exists
    # print(os.listdir(".")) # ['main.sh', 'src', 'public', '.git', '.gitignore', 'test.sh', 'special', 'static']

main()