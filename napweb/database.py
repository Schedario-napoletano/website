import enum

import sqlalchemy as sa
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import TSVECTOR
from flask_sqlalchemy import SQLAlchemy

from napweb.app import app
from napweb.utils import slugify

db = SQLAlchemy(app)


# https://amitosh.medium.com/full-text-search-fts-with-postgresql-and-sqlalchemy-edc436330a0c
# noinspection PyAbstractClass
class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR


class DefinitionType(enum.Enum):
    default = 1
    alias = 2
    variation = 3


class Definition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Unicode, unique=True, nullable=False, index=True)
    slug = db.Column(db.Unicode, unique=True, nullable=False, index=True,
                     default=lambda ctx: slugify(ctx.get_current_parameters()["word"]))

    # use an int instead of an enum type because it’s a nightmare to change later
    definition_type = db.Column(db.SmallInteger, server_default=sa.text(str(DefinitionType.default.value)))

    qualifier = db.Column(db.String, nullable=True)
    definition = db.Column(db.UnicodeText, nullable=True)

    # for aliases
    target = db.Column(db.Unicode, nullable=True)

    # https://amitosh.medium.com/full-text-search-fts-with-postgresql-and-sqlalchemy-edc436330a0c
    __ts_vector__ = db.Column(TSVector(),
                              db.Computed("to_tsvector('italian', word || ' ' || definition)", persisted=True))
    __table_args__ = (Index('ix_definition___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)
