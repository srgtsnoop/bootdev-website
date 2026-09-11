import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")


def copy_static(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_static(source_path, destination_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} " f"using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
    basepath,
):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if entry.endswith(".md"):
                dest_path = os.path.splitext(dest_path)[0] + ".html"

                generate_page(
                    source_path,
                    template_path,
                    dest_path,
                    basepath,
                )

        else:
            generate_pages_recursive(
                source_path,
                template_path,
                dest_path,
                basepath,
            )


generate_pages_recursive(
    "content",
    "template.html",
    "public",
    "/",
)


def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
    basepath,
):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if entry.endswith(".md"):
                dest_path = os.path.splitext(dest_path)[0] + ".html"

                generate_page(
                    source_path,
                    template_path,
                    dest_path,
                    basepath,
                )

        else:
            generate_pages_recursive(
                source_path,
                template_path,
                dest_path,
                basepath,
            )


def main():
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    source = "static"
    destination = "docs"

    if os.path.exists(destination):
        shutil.rmtree(destination)

    copy_static(source, destination)

    generate_pages_recursive(
        "content",
        "template.html",
        destination,
        basepath,
    )


main()
