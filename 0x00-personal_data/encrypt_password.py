#!/usr/bin/env python3
"""
  Provides a function that prevents password from
  being stored in plain text in a databse
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ a function used to encrypt a password """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)

    return hashed_pwd
