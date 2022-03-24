from flask import render_template, g, abort, url_for, redirect
from flask_sqlalchemy import Pagination

from .app import app
from .database import Definition, get_prev_next_definitions, type2enum

LETTERS = "A B C D E F G H I J L M N O P Q R S T U V Z".split(" ")
PAGE_SIZE = 150


@app.before_request
def populate_g():
    g.letters = LETTERS
    g.definition_types = type2enum


@app.route("/")
def home():
    return render_template("home.html.j2")


@app.route("/lettera/<letter>")
def letter_index(letter, page=None):
    if letter not in LETTERS:
        abort(404)

    if page is None:
        page = 1

    definitions_query = Definition.query.filter(Definition.initial_letter == letter).order_by(Definition.id)
    # error_out makes it return a 404 if there are no items or the page is wrong (e.g. negative)
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
    pagination: Pagination = definitions_query.paginate(page, per_page=PAGE_SIZE, error_out=True)

    sub_title = f"{letter} (pagina {page})" if page > 1 else letter

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
    return render_template("letter.html.j2", letter=letter, pagination=pagination, sub_title=sub_title)


@app.route("/lettera/<letter>/pagina/<int:page>")
def paginated_letter_index(letter, page):
    if page < 1:
        abort(404)

    # /lettera/X/pagina/1 should be /lettera/X
    if page == 1:
        return redirect(url_for("letter_index", letter=letter))

    return letter_index(letter, page=page)


@app.route("/parola/<slug>")
def word_page(slug):
    # TODO prev / next definitions
    definition = Definition.query.filter(Definition.slug == slug).limit(1).first_or_404()

    prev_definition, next_definition = get_prev_next_definitions(definition)

    return render_template("word.html.j2",
                           definition=definition,
                           prev_definition=prev_definition,
                           next_definition=next_definition)


@app.route("/a-proposito")
def a_proposito():
    return render_template("about.html.j2")


@app.route("/abbreviazioni")
def abbreviations():
    return render_template("abbreviations.html.j2",
                           sub_title="Abbreviazioni")
