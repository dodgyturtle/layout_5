import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def generate_html():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    with open("json/book_desc.json", "r") as book_description_file:
        book_description = book_description_file.read()

    books = json.loads(book_description)
    rendered_page = template.render(books=books)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def on_reload():
    server = Server()
    server.watch("json/book_desc.json", generate_html)
    server.serve(root=".",)


if __name__ == "__main__":
    generate_html()
    on_reload()
