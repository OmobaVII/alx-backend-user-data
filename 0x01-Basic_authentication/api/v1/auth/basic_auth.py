#!/usr/bin/env python3
""" This module provides the class BasicAuth """
from api.v1.auth.auth import Auth


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
