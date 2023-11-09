#!/usr/bin/env python3
""" Creates a new model UserSession """
from models.base import Base


class UserSession(Base):
    """ defiines the class UserSession """
    def __init__(self, *args: list, **kwargs: dict):
        """ initializes the class """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
