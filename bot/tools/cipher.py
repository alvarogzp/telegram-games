import os

from Crypto.Hash import SHA512


# Reinitialized on restart
RANDOM_SALT = os.urandom(64)


def salted_digest(data):
    hasher = SHA512.new()
    hasher.update(data)
    hasher.update(RANDOM_SALT)
    return hasher.hexdigest()
