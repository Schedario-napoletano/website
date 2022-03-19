import sys
import argparse

import json

from napweb.database import db, definition_from_dict


def main():
    p = argparse.ArgumentParser()
    p.parse_args()

    slugs = {}

    for definition_dict in json.load(sys.stdin):
        definition = definition_from_dict(definition_dict)

        if definition.slug in slugs:
            raise RuntimeError(f"Conflicting slug {definition.slug} for {slugs[definition.slug]} and {definition.word}")

        slugs[definition.slug] = definition.word

        db.session.add(definition)

    db.session.commit()


if __name__ == '__main__':
    main()
