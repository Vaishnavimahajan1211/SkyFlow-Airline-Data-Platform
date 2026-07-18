"""
Common Helper Functions
"""

import random
import string


def generate_code(prefix, length=5):

    characters = string.ascii_uppercase + string.digits

    random_part = ''.join(random.choices(characters, k=length))

    return f"{prefix}{random_part}"