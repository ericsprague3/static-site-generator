import os

from block import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the template file exists before starting
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found at: {template_path}")

    # os.walk automatically crawls through all subdirectories recursively
    for root, dirs, files in os.walk(dir_path_content):
        print(f"files: {files}")
        for file in files:
            # Check if the file is a markdown file
            if file.endswith(".md") or file.endswith(".markdown"):
                # 1. Full path to the source markdown file (e.g., 'content/blog/posts/hello.md')
                from_path = os.path.join(root, file)
                
                # 2. Get the relative structure from the content root (e.g., 'blog/posts/hello.md')
                rel_path = os.path.relpath(from_path, dir_path_content)
                
                # 3. Safely swap .md for .html while keeping the path intact
                base_path, _ = os.path.splitext(rel_path)
                rel_html_path = base_path + ".html"
                
                # 4. Map it to the final destination directory (e.g., 'public/blog/posts/hello.html')
                dest_path = os.path.join(dest_dir_path, rel_html_path)
                print(f"dest_path: {dest_path}")
                
                # 5. Hand it off to your page generator
                # (Your generate_page function automatically handles os.makedirs for subfolders!)
                generate_page(from_path, template_path, dest_path)



def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")