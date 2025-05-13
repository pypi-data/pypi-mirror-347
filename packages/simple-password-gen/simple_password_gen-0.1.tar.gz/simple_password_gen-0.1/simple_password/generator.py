import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True):
    chars = list(string.ascii_lowercase)
    
    if use_uppercase:
        chars += list(string.ascii_uppercase)
    if use_digits:
        chars += list(string.digits)
    if use_symbols:
        chars += list("!@#$%^&*()-_=+[]{};:,.<>?/")

    if not chars:
        raise ValueError("Character set cannot be empty. Enable at least one option.")

    return ''.join(random.choice(chars) for _ in range(length))
