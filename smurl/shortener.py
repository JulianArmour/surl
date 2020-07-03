alphabet = "bcdfghjkmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"
char_index = {char: i for i, char in enumerate(alphabet)}


def base_39_encode(number):
    if number == 0:
        return "b"

    encoding = []
    while number > 0:
        encoding.append(alphabet[number % 39])
        number //= 39
    return "".join(reversed(encoding))


def base_39_decode(base_39_str):
    return sum(
        char_index[char] * 39 ** i for i, char in enumerate(reversed(base_39_str))
    )


def reverse_32(num):
    """
    reverses the bits representing the number
    :param num: a number treated as being 32 bits long
    :return: the reversed number
    """
    result = 0
    for i in range(32):
        result <<= 1
        result |= num & 1
        num >>= 1
    return result
