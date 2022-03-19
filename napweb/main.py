from flask import render_template, g, abort
from flask_assets import Environment
from webassets import Bundle

from .app import app
from .database import Definition, type2enum

app.jinja_options["autoescape"] = lambda _: True

assets = Environment(app)
# js = Bundle(...,
#             filters='jsmin', output='static/js/main.min.js')
# assets.register('js_all', js)

sass = Bundle('sass/main.scss', filters='libsass', output='css/sass.css')
all_css = Bundle(sass, filters='rcssmin', output="css/main.min.css")
assets.register('css_all', all_css)

LETTERS = "A B C D E F G H I J L M N O P Q R S T U V Z".split(" ")


@app.before_request
def populate_g():
    g.letters = LETTERS
    g.definition_types = type2enum


@app.route("/")
def home():
    return render_template("home.html.j2")


@app.route("/lettera/<letter>")
def letter_index(letter):
    # TODO pagination
    if letter not in LETTERS:
        abort(404)

    definitions = Definition.query.filter(Definition.initial_letter == letter).all()

    return render_template("letter.html.j2", letter=letter, definitions=definitions)


@app.route("/parola/<slug>")
def word_page(slug):
    # TODO prev / next definitions
    definition = Definition.query.filter(Definition.slug == slug).limit(1).first_or_404()
    return render_template("word.html.j2", definition=definition)


@app.route("/a-proposito")
def a_proposito():
    return render_template("about.html.j2")
