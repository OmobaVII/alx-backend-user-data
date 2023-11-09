#!/usr/bin/env python3
""" Provides the class SessionExpAuth that inherits
    from SessionAuth
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ adds an expiration date to a session id """
    def __init__(self):
        """ defines the class """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
            self.session_duration
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates a session id """
        ses_id = super().create_session(user_id)
        if not ses_id:
            return None
        self.user_id_by_session_id[ses_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return ses_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user_id from the sesion dictionary """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.key.get(session_id).get('user_id')
        if 'created_at' not in self.user_id_by_session_id.keys():
            return None
        created_at = self.user_id_by_session_id['created_at']
        exp_time = created_at + timedelta(seconds=self.session_duration)

        if exp_time < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get('user_id')
