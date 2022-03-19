from flask import render_template, g
from flask_assets import Environment
from webassets import Bundle

from .app import app

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


@app.route("/")
def home():
    return render_template("home.html.j2")


@app.route("/lettera/<letter>")
def letter_index(letter):
    return render_template("letter.html.j2", letter=letter)

@app.route("/parola/<slug>")
def word_page(slug):
    # TODO
    return render_template("word.html.j2")


@app.route("/a-proposito")
def a_proposito():
    return render_template("about.html.j2")
