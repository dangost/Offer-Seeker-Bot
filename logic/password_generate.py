import random

chars = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPQqRrSstTuUvVwWxXYyZz0123456789'


def get_pass(length=8):
    password = ''
    for i in range(length):
        password += random.choice(chars)
    return password
