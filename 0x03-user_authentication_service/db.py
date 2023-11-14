#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ save the user to the database """
        try:
            if email is None or hashed_password is None:
                return

            user = User(email=email, hashed_password=hashed_password)
            if user is None:
                return
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            return None

    def find_user_by(self, **kwargs: dict) -> User:
        """ Finds a user in the db based on the keyword argument """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
