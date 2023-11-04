# Built-In
import re
import logging

# Third party
import streamlit as st

# Project
from streamproto.utils import loggerutils


# loggerutils.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


class InvalidEmailException(Exception):
    pass


def is_valid(email: str):
    return re.compile(
        '^[a-zA-Z0-9+-_.]+'
        '@[a-zA-Z0-9-]+'
        '\.[a-zA-Z0-9-.]+$'
    ).match(email)


class SessionEmail():

    def __new__(cls, id_: str):
        # TODO: Add StreamSession class and Inherit it.
        k = f'{id_}_session_state'
        if k not in st.session_state:
            obj = super().__new__(cls)
            obj.__init__(id_)
            obj._is_valid = False
            st.session_state[k] = obj
        return st.session_state[k]

    def __init__(self, id_: str):
        self.name = id_
        self._email = ''

    @property
    def is_valid(self):
        return self._is_valid

    @is_valid.setter
    def is_valid(self, v: bool):
        logger.debug(f'{self.name} setter called ({self.is_valid} to {v})')
        self._is_valid = v

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, v: str):
        self._email = v
        if not is_valid(v):
            self.is_valid = False
            raise InvalidEmailException(v)
        self.is_valid = True

    def check(self, text_input_key: str):
        def f():
            try:
                self.email = st.session_state[text_input_key]
            except InvalidEmailException:
                pass
            logger.debug(f'Check the email is valid: {self.is_valid}')
            return self.is_valid
        return f
