import enum
from typing import Dict, Optional

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

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


def definition_from_dict(d: dict):
    definition = Definition(
        word=d["word"],
        slug=slugify(d["word"]),
        definition_type=type2enum[d["definition_type"]],
        initial_letter=d["initial_letter"],
        qualifier=d.get("qualifier"),
        definition=d.get("definition"),
        target_text=d.get("target"),
    )

    return definition
