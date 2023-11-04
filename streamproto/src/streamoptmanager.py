# Built-In
import logging
from typing import Union

# Third party
import streamlit as st

# Project
from streamproto.core.streamoption import Option
from streamproto.components import streamform
from streamproto.utils import loggerutils


# loggerutils.set_basic_config(logging.DEBUG)
logger = logging.getLogger(__name__)


class DependentSingleOptionManager(streamform.BaseFormState):

    def __init__(
        self,
        name: str,
        options: list[Option],
        n_selectable_components_in_first_render: int = 1
    ):
        super().__init__(name)
        self.options = options
        self.n_selectable_components_in_first_render = \
            n_selectable_components_in_first_render

    @property
    def n_holden_options(
        self
    ) -> int:
        return len([e for e in self.options if e.has_holder])

    def get_option_holden_by(
        self,
        holder: str
    ) -> Option:
        for e in self.options:
            if e.holder_is(holder):
                return e
        return None

    def give_option_to(
        self,
        option: Option,
        holder: str
    ):
        option.is_visible = False
        option.holder = holder

    def release_option(
        self,
        option: Option
    ):
        option.holder = None
        option.is_visible = True

    def change_option_holder(
        self,
        holder: str,
        new_holder: str
    ):
        option = self.get_option_holden_by(holder)
        self.give_option_to(option, new_holder)

    def selectable_options(self, key: str):
        selectable = [
            e for e in self.visible_options
            if (not e.has_holder) or e.holder_is(key)
        ]
        if self.get_option_holden_by(key) is None:
            # NOTE: Initial rendering
            self.give_option_to(selectable[0], key)
            logger.debug(f'{key}:\tSet `{selectable[0]}` as a holding')
            if ((p:=self.n_holden_options) <=
                (q:=self.n_selectable_components_in_first_render)):
                # Initially, when Streamlit runs this code block,
                # it doesn't have information about
                # options that will be held by other select boxes.
                # However, we have specified
                # the total number of select boxes in advance,
                # so we skip to allow this select boxes utilize q - p + 1 options.
                selectable = selectable[q-p+1:]
        holding = self.get_option_holden_by(key)
        selectable = [holding] + selectable
        return selectable

    @property
    def visible_options(self):
        return [e for e in self.options if e.is_visible]

    @property
    def unvisible_options(self):
        return [e for e in self.options if not e.is_visible]

    def get(self, v: Union[str, Option]) -> Option:
        for e in self.options:
            if e == v:
                return e
        raise RuntimeError(
            f'Nothing matched with {v}({type(v)})'
        )

    def check(self, key: str):
        def f():
            prev = self.get_option_holden_by(key)
            self.release_option(prev)
            new = st.session_state[key]
            self.give_option_to(new, key)
            logger.debug(f'{key}:\t `{repr(prev)}`\t-> `{repr(new)}`')
        return f

    def initialize(self):
        for e in self.options:
            e.initialize()


def example():
    options = [
        Option('Math', vis_string='🧮 Math (grade: A+)'),
        Option('English', vis_string='🇬🇧 English (grade: B+)'),
        Option('Korean', vis_string='🇰🇷 Korean (grade: C+)'),
        Option('French', vis_string='🇫🇷 French (grade: D+)'),
        Option('Computer', vis_string='💻 Computer (grade: A+)')
    ]
    option_manager = DependentSingleOptionManager(
        'score_option', options,
        n_selectable_components_in_first_render = 3
    )
    key = 'selectbox_primary'
    if (options:=option_manager.selectable_options(key)):
        st.selectbox(
            'Your Favorite Subject',
            options,
            key=key,
            on_change=option_manager.check(key)
        )
    key = 'selectbox_secondary'
    if (options:=option_manager.selectable_options('selectbox_secondary')):
        st.selectbox(
            'Secondary Subject',
            options,
            key=key,
            on_change=option_manager.check(key)
        )
    key = 'selectbox_teritary'
    if (options:=option_manager.selectable_options('selectbox_teritary')):
        st.selectbox(
            'Tertiary Subject',
            options,
            key=key,
            on_change=option_manager.check(key)
        )
    st.button('initialize', on_click=option_manager.initialize)


if __name__ == '__main__':
    example()
