import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

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
