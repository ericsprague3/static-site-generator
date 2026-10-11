from textnode import TextNode, TextType
from finder import extract_markdown_links, extract_markdown_images

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_list.append(old_node)
        else:
            # check if delimiter exists evenly or it is invalid
            delimiter_count = old_node.text.count(delimiter)
            if delimiter_count % 2 == 1:
                raise ValueError(f"Invalid markdown, delimiter {delimiter} not properly closed")

            split_parts = old_node.text.split(delimiter)
            if len(split_parts) > 0:
                for index in range(len(split_parts)):
                    val = split_parts[index]
                    if index % 2 == 0:
                        new_list.append(TextNode(val, TextType.TEXT))
                    else:
                        new_list.append(TextNode(val, text_type))
            else:
                # No delimiter found in text, add as is
                new_list.append(old_node)

    return new_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    old_nodes = [TextNode(text, TextType.TEXT)]
    old_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    old_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
    old_nodes = split_nodes_delimiter(old_nodes, '`', TextType.CODE)
    old_nodes = split_nodes_image(old_nodes)
    old_nodes = split_nodes_link(old_nodes)
    return old_nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    sections = markdown.split("\n\n")
    final_list = []
    for item in sections:
        stripped_item = item.strip()
        if stripped_item != "":
            final_list.append(item.strip())

    return final_list