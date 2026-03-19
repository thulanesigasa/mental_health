from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password):
    return ph.hash(password)

def verify_password(hashed, password):
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False
