import os

from flask import Flask

app = Flask(__name__)
# Dokku uses postgres:// but SQLAlchemy 1.4+ supports only postgresql://
# https://stackoverflow.com/a/66794960/735926
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CANONICAL_DOMAIN'] = os.environ.get("CANONICAL_DOMAIN")
app.config['HTTPS'] = os.environ.get('HTTPS')

app.jinja_options["autoescape"] = lambda _: True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

if os.environ.get("DEBUG"):
    app.debug = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
