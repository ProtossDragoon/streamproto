# External
import re
import logging

# Third party
import streamlit as st

# Project
from utils import loggerutils


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
        k = f'{id_}_session_state'
        if k not in st.session_state:
            obj = super().__new__(cls)
            obj.__init__(id_)
            st.session_state[k] = obj
        return st.session_state[k]

    def __init__(self, id_: str):
        self.name = id_
        self._email = ''
        self._is_valid = False

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
            return self.is_valid
        return f


def example():
    se = SessionEmail('user1')
    email1 = st.text_input(
        '[User1] Email input',
        value=se.email,
        key='user1_input1',
        on_change=se.check('user1_input1'),
        placeholder='example@google.com'
    )

    if se.is_valid:
        st.caption('... 👏')
        se = SessionEmail('user1')
        email2 = st.text_input(
            '[User1] Automatically filled Email input',
            value=se.email,
            key='user1_input2',
            on_change=se.check('user1_input2'),
            placeholder='example@google.com'
        )
        if se.is_valid:
            st.caption('..... 👏')
        else:
            st.caption('..... ⛔️ (invalid Email address)')

        se = SessionEmail('user2')
        email3 = st.text_input(
            '[User2] Another user\'s Email input',
            value=se.email,
            key='user2_input1',
            on_change=se.check('user2_input1'),
            placeholder='example@google.com'
        )
        if se.is_valid:
            st.caption('..... 👏')
        else:
            st.caption('..... ⛔️ (invalid Email address)')

    else:
        st.caption('... ⛔️ (invalid Email address)')


if __name__ == '__main__':
    example()
