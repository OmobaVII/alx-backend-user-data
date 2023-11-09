#!/usr/bin/env python3
""" creates a class SessionDBAuth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ defines the class """
    def create_session(self, user_id=None):
        """ creates and stores new instances of UserSession """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        dic = {'user_id': user_id, 'session_id': session_id}
        user_ses = UserSession(**dic)
        user_ses.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns the User ID by requsting UserSession """
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_ses = UserSession.search({'session_id': session_id})
        if not user_ses:
            return None
        user_ses = user_ses[0]

        exp_time = user_ses.created_at +\
            timedelta(seconds=self.session_duration)

        if exp_time < datetime.now():
            return None

        return user_ses.user_id

    def destroy_session(self, request=None):
        """ deletes a session from the database """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_ses = UserSession.search({'session_id': session_id})

        if not user_ses:
            return False

        user_ses = user_ses[0]

        try:
            user_ses.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
