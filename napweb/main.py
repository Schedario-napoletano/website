import htmlmin
from flask import render_template, g, abort, url_for, redirect, request
from flask_sqlalchemy import Pagination
from flask_assets import Environment
from webassets import Bundle

from .app import app
from .database import Definition, get_prev_next_definitions, type2enum, search_definitions

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
MAX_SEARCH_RESULTS = 50


@app.before_request
def populate_g():
    g.letters = LETTERS
    g.definition_types = type2enum


@app.after_request
def minify_html(response):
    if not app.debug and response.content_type.startswith("text/html"):
        response.set_data(
            htmlmin.minify(response.get_data(as_text=True),
                           remove_comments=True,
                           remove_empty_space=True)
        )

    return response


@app.errorhandler(404)
def page_not_found(_e):
    return render_template("404.html.j2", sub_title="404"), 404


@app.errorhandler(500)
def server_error(_e):
    return render_template("500.html.j2", sub_title="500"), 500


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
    definition = Definition.query.filter(Definition.slug == slug).limit(1).first_or_404()

    prev_definition, next_definition = get_prev_next_definitions(definition)

    return render_template("word.html.j2",
                           definition=definition,
                           prev_definition=prev_definition,
                           next_definition=next_definition)


@app.route("/ricerca")
def search():
    query = request.args.get("q", "")

    definitions = search_definitions(query, limit=MAX_SEARCH_RESULTS)

    return render_template("search.html.j2",
                           sub_title="Ricerca",
                           definitions=definitions,
                           definitions_count=len(definitions),
                           maximum_count=MAX_SEARCH_RESULTS,
                           search_query=query)
    # TODO
    # https://amitosh.medium.com/full-text-search-fts-with-postgresql-and-sqlalchemy-edc436330a0c
    # https://github.com/recrsn/video-gallery/blob/master/migrations/versions/7f9863909887_.py


@app.route("/ricerca/aiuto")
def search_help():
    return render_template("search_help.html.j2", sub_title="Aiuto per la ricerca")


@app.route("/a-proposito")
def a_proposito():
    return render_template("about.html.j2", sub_title="A proposito")


@app.route("/abbreviazioni")
def abbreviations():
    return render_template("abbreviations.html.j2", sub_title="Abbreviazioni usate")


@app.route("/introduzione")
def introduction():
    return render_template("intro.html.j2", sub_title="Introduzione", page_class="intro")
