from slugify import slugify as slugify_


def slugify(text: str) -> str:
    # slugify_() drops the initial spaces/hyphens. We had an 'x' at the beginning to force them to be preserved then
    # remove it after that.
    # noinspection PyArgumentList
    slug = slugify_("x" + text,
                    allow_unicode=True,
                    lowercase=False,
                    replacements=(("'", "-"),
                                  ("’", "-"),
                                  ("‘", "-")))
    if slug.startswith("x"):
        slug = slug[1:]
    return slug
