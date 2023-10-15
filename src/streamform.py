# External
import logging
from collections.abc import Callable

# Third party
import streamlit as st

# Project
import streamail
from utils import loggerutils


loggerutils.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseFormState():

    def __new__(
        cls,
        name: str,
        se: streamail.SessionEmail = None
    ):
        k = f'{name}_session_state'
        if k not in st.session_state:
            obj = super().__new__(cls)
            obj.__init__(name, se)
            st.session_state[k] = obj
        return st.session_state[k]

    def __init__(
        self,
        name: str,
        se: streamail.SessionEmail = None
    ):
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


class ExampleSequentialFormState(BaseFormState):

    def __init__(
        self,
        name: str,
        se: streamail.SessionEmail = None
    ) -> None:
        super().__init__(name, se)
        self.show_toggle = True
        self.default_q1_answer = 'Please select!'
        self.trigger_q1a_answer = 'Type manually'
        self.q1_finished = False
        self._q1a_typing = False
        self.show_q2 = False
        self.finished = False

    @property
    def q1a_empty(self) -> bool:
        if self.q1a_typing:
            return self._q1a_typing
        else:
            return False

    def state_q1_changing(self):
        self.show_toggle = True
        self.q1_finished = False
        self.show_q2 = False
        self.finished = False

    def state_q1a_changing(self):
        self.show_toggle = True
        self.q1a_typing = True
        self.q1_finished = False
        self.show_q2 = False
        self.finished = False

    def state_q1_finished(self):
        self.show_toggle = True
        self.q1a_typing = False
        self.q1_finished = True
        self.show_q2 = True
        self.finished = False

    @if_valid_email
    def state_finished(self):
        self.show_toggle = False
        self.q1_finished = True
        self.show_q2 = False
        self.finished = True


def example():
    form = ExampleSequentialFormState('exform')
    with st.expander(
        f'{"💡" if form.show_toggle else "✅"} I have a question!',
        expanded=form.show_toggle
    ):
        # q1
        feature = st.selectbox(
            '[q1] What do you want?', [
                form.default_q1_answer,
                'feature A',
                'feature B',
                'feature C',
                form.trigger_q1a_answer,
                ],
            on_change=form.state_q1_changing
        )
        # q1-a
        if feature == form.trigger_q1a_answer:
            manual_feature = st.text_input(
                'manual input',
                placeholder='📝',
                label_visibility='collapsed',
                on_change=form.state_q1a_changing,
            )
        st.button(
            '[q1] Submit',
            disabled=(
                form.q1_finished or
                (feature == form.default_q1_answer)
            ),
            on_click=form.state_q1_finished,
            use_container_width=True
        )
        if form.show_q2:
            email = st.text_input(
                '[q2] I will notify you',
                value=form.se.email,
                key=form.se.name,
                on_change=form.se.check(form.se.name),
                placeholder='example@google.com')
            st.button(
                '[q2] Submit',
                on_click=form.state_finished(email=email),
                use_container_width=True
            )
            if not (form.se.is_valid):
                st.caption('... ⛔️ (invalid Email address)')


if __name__ == '__main__':
    example()
