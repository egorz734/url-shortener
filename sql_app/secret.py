import random
import string


def make_short_url() -> str:
    uniqueValues = string.ascii_letters + string.digits
    return ''.join(random.choices(uniqueValues, k=6))
