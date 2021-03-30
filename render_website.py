import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def load_book_description(filepath: str) -> dict:
    with open(filepath, "r") as book_description_file:
        book_description = book_description_file.read()
    book_description = json.loads(book_description)
    return book_description


def generate_html(
    book_description: dict, directorypath: str, filepath_template: str = "template.html"
):
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(filepath_template)
    chunked_books = chunked(book_description, 2)
    book_index_pages = chunked(chunked_books, 20)
    for index_filename, book_index_page in enumerate(book_index_pages):
        rendered_page = template.render(chunked_books=book_index_page)
        index_filename = f"index{index_filename}.html"
        index_filepath = os.path.join(directorypath, index_filename)
        with open(index_filepath, "w", encoding="utf8") as file:
            file.write(rendered_page)


def on_reload(
    watched_file: str,
    root_directory: str = ".",
    default_index_filename: str = "pages/index0.html",
):
    server = Server()
    server.watch(watched_file, generate_html)
    server.serve(root=root_directory, default_filename=default_index_filename)


def main():
    index_directory = "pages"
    book_description_filepath = "json/book_desc.json"
    book_description = load_book_description(book_description_filepath)
    os.makedirs(index_directory, exist_ok=True)
    generate_html(book_description, index_directory)
    on_reload(book_description_filepath)


if __name__ == "__main__":
    main()
