#!/usr/bin/env python3
""" This module provide a function `filter_datum` and a class """
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ class constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records using filter_datum """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """ returns a logging.Logger Object """
    first_log = logging.getLogger("user_data")
    first_log.setLevel(logging.INFO)
    first_log.propagate = False

    stream = logging.StreamHandler()
    formatting = RedactingFomatter(PII_FIELDS)
    stream.setFormatter(formatting)
    first_log.addHandler(stream)

    return first_log
