import os
from block_markdown import markdown_to_html_node

def extract_title(markdown:str):
    if markdown.startswith("# "):
        return markdown[1:].strip()
    raise Exception("No h1 header found.")

def generate_page(from_path:str, template_path:str, dest_path:str):
    print(f"Generating page from {from_path}, to {dest_path}, using {template_path}.")
    markdown_content = open(from_path).read()
    template_content = open(template_path).read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    open(dest_path, "w").write(template_content)