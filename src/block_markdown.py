from enum import Enum

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        stripped = raw_block.strip()
        if stripped == "":
            continue
        blocks.append(stripped)
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        expected_number = 1
        for line in lines:
            if not line.startswith(f"{expected_number}. "):
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children.append(ParentNode("p", text_to_children(text)))

        elif block_type == BlockType.HEADING:
            level = 0

            for char in block:
                if char == "#":
                    level += 1
                else:
                    break

            text = block[level:].strip()

            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif block_type == BlockType.CODE:
            text = block[3:-3]

            if text.startswith("\n"):
                text = text[1:]

            code_node = LeafNode("code", text)
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_lines = []

            for line in lines:
                quote_lines.append(line.lstrip(">").strip())

            text = " ".join(quote_lines)

            children.append(ParentNode("blockquote", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []

            for line in block.split("\n"):
                text = line[2:]
                items.append(ParentNode("li", text_to_children(text)))

            children.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            items = []

            for line in block.split("\n"):
                text = line.split(". ", 1)[1]

                items.append(ParentNode("li", text_to_children(text)))

            children.append(ParentNode("ol", items))

    return ParentNode("div", children)
