#!/usr/bin/env python3
""" This module provides the class Auth """
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


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
        if p in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

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

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if request is None:
            return None
        _my_session_id = request.cookies.get(getenv('SESSION_NAME'))
        return _my_session_id
