import os

from Crypto.Hash import SHA256

# Reinitialized on restart
RANDOM_SALT = os.urandom(64)


def salted_digest(data):
    hasher = SHA256.new()
    hasher.update(data)
    hasher.update(RANDOM_SALT)
    return hasher.digest()
