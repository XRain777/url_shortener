# https://stackoverflow.com/questions/1119722/base-62-conversion
# используется алфавит адресов Bitcoin (https://ru.wikipedia.org/wiki/Base58)

import string
BASE_LIST = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

def base_decode(string, reverse_base=BASE_DICT):
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(string[::-1]):
        ret += (length ** i) * reverse_base[c]

    return ret

def base_encode(integer, base=BASE_LIST):
    if integer == 0:
        return base[0]

    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer //= length

    return ret