#!/usr/bin/env python3
""" Creates a class SessionAuth that inherits from Auth """
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ defines the class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for user_id """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a user id based on a session id """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on cookie value """
        if request is None:
            request = request

        u_ses_id = self.session_cookie(request)

        if u_ses_id is None:
            return None
        else:
            u_id = self.user_id_for_session_id(u_ses_id)
        if u_id is None:
            return None
        else:
            return User.get(u_id)

    def destroy_session(self, request=None):
        """ deletes the user session """
        if request is None:
            return False
        ses_id = self.session_cookie(request)
        if ses_id is None:
            return False
        u_id = self.user_id_for_session_id(ses_id)
        if u_id is None:
            return False
        del self.user_id_by_session_id[ses_id]
        return True
