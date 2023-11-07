#!/usr/bin/env python3
""" This module provides the class BasicAuth """
from api.v1.auth.auth import Auth
import base64


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
