# Built-In
import logging
from collections.abc import Callable

# Third party
import streamlit as st

# Project
from streamproto.utils import loggerutils
from streamproto.components import streamail


# loggerutils.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseSessionFormState():

    def __new__(
        cls,
        name: str,
        *args,
        se: streamail.SessionEmail = None,
        **kwargs
    ):
        # TODO: Add StreamSession class and Inherit it.
        k = f'{name}_session_state'
        if k not in st.session_state:
            obj = super().__new__(cls)
            st.session_state[k] = obj
        return st.session_state[k]

    def __init__(
        self,
        name: str,
        se: streamail.SessionEmail = None
    ):
        logger.debug('__init__() called.')
        self.name = name
        if se is None:
            se = streamail.SessionEmail(name+'_email')
        self.se = se


def if_valid_email(do_sth: Callable) -> Callable:
    def f(*args, **kwargs):
        email = kwargs.pop('email')
        if streamail.is_valid(email):
            return do_sth(*args, **kwargs)
        else:
            def do_nothing():
                pass
            return do_nothing
    return f
