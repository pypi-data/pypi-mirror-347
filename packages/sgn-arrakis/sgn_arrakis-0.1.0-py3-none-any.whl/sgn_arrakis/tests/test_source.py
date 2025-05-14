from sgn_arrakis import ArrakisSource, __version__


def test_version():
    assert __version__ != "?.?.?"
    assert ArrakisSource is not None
