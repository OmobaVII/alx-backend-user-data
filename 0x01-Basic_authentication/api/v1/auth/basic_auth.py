#!/usr/bin/env python3
""" This module provides the class BasicAuth """
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ defines the class BasicAuth which inherits from Auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns a Base64 part of the AUthorization header """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        end_part = authorization_header.replace('Basic ', '', 1)

        return end_part

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64.b64encode(base64.b64decode(base64_authorization_header))
        except Exception:
            return None

        return base64.b64decode(base64_authorization_header).decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ returns the user email and password from Base64 decoded value """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        username = decoded_base64_authorization_header.split(':')[0]
        password = decoded_base64_authorization_header.split(':')[1]

        return username, password

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            user = User.search({'email': user_email})
        except Exception:
            return None

        if not user:
            return None

        for u in user:
            if u.is_valid_password(user_pwd):
                return u
            else:
                return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        if request is None:
            return None
        authorization_header = super().authorization_header(request)
        if authorization_header is None:
            return None
        base64 = self.extract_base64_authorization_header(authorization_header)
        if base64 is None:
            return None
        try:
            decoded = self.decode_base64_authorization_header(base64)
            if decoded is None:
                return None
            extract = self.extract_user_credentials(decoded)
            if extract is None:
                return None
            user_obj = self.user_object_from_credentials(extract[0], extract[1])

            return user_obj
        except Exception:
            return None
