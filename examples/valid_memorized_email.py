import os, sys
if 'streamproto' not in sys.modules:
    sys.path.append(os.path.join('..', 'streamproto'))

# Third party
import streamlit as st

# Project
from streamproto.components import streamail


def example():
    se = streamail.SessionEmail('user1')
    email1 = st.text_input(
        '[User1] Email input',
        value=se.email,
        key='user1_input1',
        on_change=se.check('user1_input1'),
        placeholder='example@google.com'
    )

    if se.is_valid:
        st.caption('... 👏')
        se = streamail.SessionEmail('user1')
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

        se = streamail.SessionEmail('user2')
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
