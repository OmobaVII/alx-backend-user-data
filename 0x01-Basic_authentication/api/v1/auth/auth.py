#!/usr/bin/env python3
""" This module provides the class Auth """
from flask import request
from typing import List, TypeVar


class Auth:
    """ the class definition """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False if path none or not in exclude_paths """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        p = path
        if p.endswith('/'):
            pass
        else:
            p += '/'
        if p not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None or flask request object """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None or flask request object """
        return None
