#!/usr/bin/env python3
""" Authenticates inputs
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ returns bytes of salted has of the input """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password
