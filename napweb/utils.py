from slugify import slugify as slugify_


def slugify(text: str) -> str:
    # slugify_() drops the initial/trailing non-word characters. We want to preserve them to distinguish between the
    # slugs of "a" vs. "‘a" vs. "a’!".
    # noinspection PyArgumentList
    slug = slugify_("x" + text + "x",
                    allow_unicode=True,
                    lowercase=False,
                    replacements=(("'", "-"),
                                  ("’", "-"),
                                  ("‘", "-")))
    return slug[1:-1]
