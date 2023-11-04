# Built-In
from collections.abc import Callable


class Option():

    def __init__(
        self,
        comparer_string: str,
        format_func: Callable = None,
        vis_string: str = None,
        is_visible: bool = True,
        data: any = None
    ):
        assert type(comparer_string) is str
        if format_func is None:
            format_func = lambda x: x
        assert type(format_func(comparer_string)) is str
        if vis_string is None:
            vis_string = format_func(comparer_string)
        assert type(vis_string) is str

        self.comparer_string = comparer_string
        self.format_func = format_func
        self._vis_string = vis_string
        self.initial_visibility = is_visible
        self.is_visible = is_visible
        self.data = data
        self.holder = None

    def __repr__(
        self
    ) -> str:
        return f'Option[holder:{self.holder}][id:{id(self)}]({repr(self.comparer_string)})'

    def __str__(
        self
    ) -> str:
        return self.vis_string

    def __eq__(
        self,
        __value: object
    ) -> bool:
        if type(__value) is str:
            self.comparer_string == __value
        elif isinstance(__value, Option):
            return (
                self.comparer_string ==
                __value.comparer_string
            )

    @property
    def vis_string(
        self
    ) -> str:
        return self.format_func(self._vis_string)

    @vis_string.setter
    def vis_string(
        self,
        v: str
    ):
        assert type(v) is str
        self._vis_string = v

    @property
    def has_holder(
        self
    ) -> bool:
        return self.holder is not None

    def holder_is(
        self,
        holder: str
    ) -> bool:
        return self.holder == holder

    def initialize(
        self
    ):
        self.holder = None
        self.is_visible = self.initial_visibility
