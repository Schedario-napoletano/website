from flask import render_template, g, abort, url_for, redirect
from flask_assets import Environment
from flask_sqlalchemy import Pagination
from webassets import Bundle

from .app import app
from .database import Definition, type2enum

app.jinja_options["autoescape"] = lambda _: True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

assets = Environment(app)
# js = Bundle(...,
#             filters='jsmin', output='static/js/main.min.js')
# assets.register('js_all', js)

sass = Bundle('sass/main.scss', filters='libsass', output='css/sass.css')
all_css = Bundle(sass, filters='rcssmin', output="css/main.min.css")
assets.register('css_all', all_css)

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

    definitions_query = Definition.query.filter(Definition.initial_letter == letter)
    # error_out makes it return a 404 if there are no items or the page is wrong (e.g. negative)
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
    pagination: Pagination = definitions_query.paginate(page, per_page=PAGE_SIZE, error_out=True)

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.Pagination
    return render_template("letter.html.j2", letter=letter, pagination=pagination)


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
    return render_template("word.html.j2", definition=definition)


@app.route("/a-proposito")
def a_proposito():
    return render_template("about.html.j2")
