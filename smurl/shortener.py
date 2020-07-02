alphabet = "bcdfghjkmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"


def base_39_encode(number):
    if number == 0:
        return 'b'

    encoding = []
    while number > 0:
        encoding.append(alphabet[number % 39])
        number //= 39
    return "".join(reversed(encoding))
