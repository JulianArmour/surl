import pytest

from smurl import shortener

alphabet = "bcdfghjkmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # single characters
        (0, alphabet[0]),
        (1, alphabet[1]),
        (38, "Z"),
        # two characters
        (39, "cb"),
        (40, "cc"),
        (39 * 2, "db"),
        (39 * 2 + 1, "dc"),
        (39 * 2 + 38, "dZ"),
        (39 * 3, "fb"),
        (39 * 4, "gb"),
        # three characters
        (39 ** 2, "cbb"),
        (39 ** 2 + 1, "cbc"),
        (2 * 39 ** 2, "dbb"),
        # four characters
        (39 ** 3, "cbbb"),
    ],
)
def test_base_39_encode(test_input, expected):
    assert shortener.base_39_encode(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("b", 0),
        ("c", 1),
        ("d", 2),
        ("cb", 39),
        ("cbb", 39 ** 2),
        ("ccb", 39 ** 2 + 39),
        ("ZZZZ", (38 * 39 ** 3) + (38 * 39 ** 2) + (38 * 39) + 38),
    ],
)
def test_base_39_decode(test_input, expected):
    assert shortener.base_39_decode(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, 0),
        (1, int("1" + "0" * 31, 2)),
        (2, int("01" + "0" * 30, 2)),
        (int("1" + "0" * 30 + "1", 2), int("1" + "0" * 30 + "1", 2)),
    ],
)
def test_reverse_32(test_input, expected):
    assert shortener.reverse_32(test_input) == expected
