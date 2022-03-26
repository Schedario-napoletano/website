import os

from flask import Flask

app = Flask(__name__)
# Dokku uses postgres:// but SQLAlchemy 1.4+ supports only postgresql://
# https://stackoverflow.com/a/66794960/735926
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://")

if os.environ.get("DEBUG"):
    app.debug = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
