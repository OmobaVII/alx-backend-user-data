#!/usr/bin/env python3
"""
  Provides hashed_password function that prevents password from
  being stored in plain text in a database

  Provides is_valid function that checks that the password
  matches the hashed password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ a function used to encrypt a password """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)

    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checks that the password matches the hashed password """
    try:
        return bcrypt.checkpw(password.encode(), hashed_password)
    except (ValueError, TypeError):
        return False
