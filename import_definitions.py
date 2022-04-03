import sys
import argparse

import json
from typing import Dict, Tuple, List

import re
from unidecode import unidecode

from napweb.database import db, definition_from_dict, Definition, update_definition_from_dict


def main():
    p = argparse.ArgumentParser()
    p.parse_args()

    # slug -> word
    slugs: Dict[str, str] = {}

    aliases: List[Tuple[Definition, str]] = []

    unaccented_word2definition: Dict[str, Definition] = {}

    word2definition: Dict[str, Definition] = {
        definition.word: definition
        for definition in Definition.query.all()
    }

    definitions = json.load(sys.stdin)

    print("1. import all definitions without alias targets")
    for i, definition_dict in enumerate(definitions):
        if i and i % 1000 == 0:
            print(i)

        if definition := word2definition.get(definition_dict["word"]):
            update_definition_from_dict(definition, definition_dict)
        else:
            definition = definition_from_dict(definition_dict)
            word2definition[definition.word] = definition

        if definition.slug in slugs:
            raise RuntimeError(f"Conflicting slug {definition.slug} for {slugs[definition.slug]} and {definition.word}")

        slugs[definition.slug] = definition.word

        target = definition_dict.get("target")
        if target:
            target = re.sub(r"\s*\d+$", "", target)

            aliases.append((definition, target))

        unaccented_word2definition[unidecode(definition.word)] = definition

        db.session.add(definition)

    db.session.commit()

    print(f"# 2. link {len(aliases)} aliases")
    missing = 0
    for definition, target_word in aliases:
        word = definition.word

        # Don't try to link a word to itself
        if target_word != word and target_word in word2definition:
            definition.target_id = word2definition[target_word].id
            db.session.add(definition)
            continue

        unaccented_target_word = unidecode(target_word)
        if unaccented_target_word != word and unaccented_target_word in unaccented_word2definition:
            definition.target_id = unaccented_word2definition[unaccented_target_word].id
            db.session.add(definition)
            continue

        # Those can be typos or may mean we didn’t correctly parse the target definitions
        print(f"!!!! Missing target word {definition.word} -> {target_word}")
        missing += 1

    print("missing:", missing)  # best: 318

    # Note when overriding existing definitions this can fail with "Key (slug)=(...) already exists". A quick "fix" is
    # to delete and re-create the database.
    db.session.commit()


if __name__ == '__main__':
    main()
