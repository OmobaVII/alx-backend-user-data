#!/usr/bin/env python3
""" Authenticates inputs
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returns bytes of salted has of the input """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


class Auth:
    """ Auth class to interact wit the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ adds a user into the database """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        pwd = _hash_password(password)
        user = self._db.add_user(email=email, hashed_password=pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ validates credentials """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hash_pwd = bcrypt.checkpw(password.encode(), user.hashed_password)
                if hash_pwd is True:
                    return True
                return False
        except Exception:
            return False
