import re

def extract_markdown_images(text: str) -> list[tuple]:
    extract_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extract_list


def extract_markdown_links(text: str) -> list[tuple]:
    extract_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extract_list