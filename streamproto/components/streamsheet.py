# Built-In
import os
import pytz
import json
import logging
import functools
import datetime as dt

# Third party
import streamlit as st
import gspread

# Project
from streamproto.core import streamsession
from streamproto.utils import loggerutils


# loggerutils.set_basic_config(logging.INFO)
logger = logging.getLogger(__name__)


class SessionSheet():

    def __new__(
        cls,
        file_name: str,
        service_account_json: os.PathLike, /,
        **worksheets,
    ):
        # TODO: Add StreamSession class and Inherit it.
        # FIXME: Not sure how much secure session state is.
        k = f'{file_name}_session_sheet'
        if k not in st.session_state:
            logger.info('Creating a new Object')
            obj = super().__new__(cls)
            st.session_state[k] = obj
        return st.session_state[k]

    def __init__(
        self,
        file_name: str,
        service_account_json: os.PathLike, /,
        **worksheets
    ) -> None:
        # logger.debug('__init__() called.')
        self.file_name = file_name
        assert os.path.isfile(service_account_json)
        logger.info('Connecting with Spreadsheet API Service')
        # FIXME: This should not be called multiple times
        self.service_account_json = service_account_json
        self.gc = gspread.service_account(service_account_json)
        self.sheet = self.gc.open(file_name)
        self._worksheets = {}
        if worksheets:
            self.worksheets = worksheets

    @property
    def worksheets(self):
        return self._worksheets

    @worksheets.setter
    def worksheets(self, v):
        for sheet_name, sheet_idx in v.items():
            assert type(sheet_name) is str
            assert type(sheet_idx) is int
            self._worksheets[sheet_name] = (
                self.sheet.get_worksheet(sheet_idx)
            )

    def get_worksheet(self, sheet_name: str):
        return self.worksheets.get(sheet_name)


def write_json(
    worksheet: gspread.Worksheet, /,
    add_timestamp = True,
    timezone: str = None,
    timeformat: str = '%Y/%m/%d-%H:%M:%S',
    add_sessionid = True,
    **v
) -> None:
    # TODO: Write via worksheet column mapping class
    row = []
    if add_sessionid:
        session_id = streamsession.get_session_id()
        row.append(session_id)
    if add_timestamp:
        if timezone:
            timezone = pytz.timezone(timezone)
        time = dt.datetime.now(timezone).strftime(timeformat)
        row.append(time)
    # NOTE: Do not contain unserializable types in **v
    row.append(json.dumps(v, ensure_ascii=False))
    worksheet.append_row(row)


def callback_write_json(*args, **kwargs):
    from streamproto.components import streamsheet
    @functools.wraps(streamsheet.write_json)
    def f():
        streamsheet.write_json(*args, **kwargs)
    return f
