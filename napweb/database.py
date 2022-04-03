import enum
from typing import Dict, Optional

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from unidecode import unidecode

from .app import app
from .utils import slugify

db = SQLAlchemy(app)


class DefinitionType(enum.Enum):
    default = 1
    alias = 2
    derivative = 3


type2enum: Dict[str, int] = {d.name: d.value for d in DefinitionType}


class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Unicode, unique=True, nullable=False, index=True)
    word_ascii = db.Column(db.Unicode, nullable=False, index=True,
                           default=lambda ctx: unidecode(ctx.get_current_parameters()["word"]))
    slug = db.Column(db.Unicode, unique=True, nullable=False, index=True,
                     default=lambda ctx: slugify(ctx.get_current_parameters()["word"]))

    initial_letter = db.Column(db.String(1), nullable=False, index=True)

    # use an int instead of an enum type because it’s a nightmare to change later
    # noinspection SqlAlchemyUnsafeQuery
    definition_type = db.Column(db.SmallInteger, server_default=sa.text(str(DefinitionType.default.value)))

    qualifier = db.Column(db.String, nullable=True)
    definition = db.Column(db.UnicodeText, nullable=True)

    # for aliases
    target_id = db.Column(db.Integer, db.ForeignKey('definition.id'), index=True)
    target = relationship(lambda: Definition, remote_side=id, backref='variations')
    target_text = db.Column(db.Unicode, nullable=True)


def count_definitions():
    return db.session.query(db.func.count(Definition.id)).scalar()


def get_prev_next_definitions(definition: Definition):
    # Let’s do both in one query
    surrounding_definitions = Definition.query \
        .filter((Definition.id == definition.id - 1) | (Definition.id == definition.id + 1)).all()

    prev_definition: Optional[Definition] = None
    next_definition: Optional[Definition] = None

    for surrounding_definition in surrounding_definitions:
        if surrounding_definition.id < definition.id:
            prev_definition = surrounding_definition
        else:
            next_definition = surrounding_definition

    return prev_definition, next_definition


def _escape_query_string(query_string: str):
    """Escape a query string to be used in a LIKE clause."""
    return (
        query_string
            .replace("\\\\", "\\")  # escape the escaper
            .replace("%", "\\%")  # escape %
            .replace("_", "\\_")  # escape _
            .replace("*", "%")  # allow '*' as the wildcard for any char (%)
            .replace("?", "_")  # allow '?' as the wildcard for a single char (_)
    )


def search_definitions(query_string: str, limit: Optional[int] = None, prefix=False):
    query_string = _escape_query_string(query_string.lower())

    if prefix:
        query_string += "%"

    ascii_query_string = unidecode(query_string)

    filters = (Definition.word.like(query_string)
               | Definition.word_ascii.like(ascii_query_string))

    # try "bla" in addition to "'bla"
    if len(ascii_query_string) > 2 and "'" in ascii_query_string:
        filters |= Definition.word_ascii.like(ascii_query_string.strip("'"))

    query = Definition.query.filter(filters)

    # We have no way to 'score' the results so let's sort them by alphabetical order
    query = query.order_by(Definition.word)

    if limit:
        query = query.limit(limit)

    return query.all()


def update_definition_from_dict(definition: Definition, d: dict):
    definition.word = d["word"]
    definition.word_ascii = unidecode(d["word"])
    definition.slug = slugify(d["word"])
    definition.definition_type = type2enum[d["definition_type"]]
    definition.initial_letter = d["initial_letter"]
    definition.qualifier = d.get("qualifier")
    definition.definition = d.get("definition")
    definition.target_text = d.get("target")
    return definition


def definition_from_dict(d: dict):
    return update_definition_from_dict(Definition(), d)
