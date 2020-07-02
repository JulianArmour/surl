import pytest

from smurl import shortener

alphabet = "bcdfghjkmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, alphabet[0]), (1, alphabet[1]), (len(alphabet) - 1, alphabet[-1])],
)
def test_encode_single_digit(test_input, expected):
    assert shortener.base_39_encode(test_input) == expected


def test_encode_double_digit():
    assert shortener.base_39_encode(39) == "bb"
