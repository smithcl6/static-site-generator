import os, shutil
from generate_page import generate_pages_recursive

STATIC = "./static"
PUBLIC = "./public"

def content_to_destination(directory:list[str]|None, path:str):
    if not directory:
        print("Directory is empty")
        return
    for item in directory:
        # current_path does not include ./static or ./public
        current_path = os.path.join(path, item)
        static_path = os.path.join(STATIC, current_path)
        public_path = os.path.join(PUBLIC, current_path)
        if os.path.isdir(static_path):
            os.mkdir(public_path)
            print(f"Updated directory structure: {public_path}")
            content_to_destination(os.listdir(static_path), current_path)
        else:
            shutil.copy(static_path, public_path)
            print(f"Added {item} to {public_path}")

def main():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.mkdir(PUBLIC)
    content_to_destination(os.listdir(STATIC), "")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()