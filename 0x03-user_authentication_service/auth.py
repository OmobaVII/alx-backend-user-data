#!/usr/bin/env python3
""" Authenticates inputs
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ returns bytes of salted has of the input """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def _generate_uuid() -> str:
    """ generates a uuid """
    return str(uuid4())


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
                pwd = bcrypt.checkpw(password.encode(), user.hashed_password)
                if pwd is True:
                    return True
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates a session for a user with the email """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ finds a user by session_id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroys the session by updating the user seeion id to None """
        if user_id is None:
            return
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ returns a token to reset password """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        if user:
            reset_token = _generate_uuid()
        self._db.update_user(user.email, reset_token=reset_token)
        return reset_token
