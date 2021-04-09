import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def load_books_description(file: str) -> dict:
    with open(file, "r") as books_description_file:
        books_description_content = books_description_file.read()
    books_description = json.loads(books_description_content)
    return books_description


def save_to_html(
    books_description: dict, directory_path: str, template_file: str = "template.html"
):
    books_column_count=2
    quantity_books_on_page=20
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_file)
    chunked_books = chunked(books_description, books_column_count)
    books_pages = list(chunked(chunked_books, quantity_books_on_page))
    pages_count = len(books_pages)
    for number, books_page in enumerate(books_pages, 1):
        rendered_page = template.render(
            chunked_books=books_page,
            page_number=number,
            pages_count=pages_count,
        )
        html_filename = f"bookspage{number}.html"
        html_filepath = os.path.join(directory_path, html_filename)
        with open(html_filepath, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    html_files_directory = "pages"
    books_description_file = "media/json/book_desc.json"
    root_directory = "."
    default_html_file = "pages/bookspage1.html"
    html_template='template.html'
    server = Server()
    books_description = load_books_description(books_description_file)
    os.makedirs(html_files_directory, exist_ok=True)
    server.watch(
        books_description_file, save_to_html(books_description, html_files_directory)
    )
    server.watch(
        html_template, save_to_html(books_description, html_files_directory)
    )
    server.serve(root=root_directory, default_filename=default_html_file)


if __name__ == "__main__":
    main()
