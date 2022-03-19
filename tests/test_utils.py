from napweb import utils


def test_slugify():
    assert utils.slugify("a") == "a"
    assert utils.slugify("‘a") == "-a"
    assert utils.slugify("’a") == "-a"
    assert utils.slugify("a’!") == "a-"
    assert utils.slugify("Ciao ciao") == "Ciao-ciao"
    assert utils.slugify("ûnìcödé") == "ûnìcödé"
    assert utils.slugify("xx") == "xx"
