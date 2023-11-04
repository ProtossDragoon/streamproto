import os, sys
if 'streamproto' not in sys.modules:
    sys.path.append(os.path.join('..', 'streamproto'))

# Third party
import streamlit as st

# Project
from streamproto.components import streamsheet


def example(
    service_account_json: os.PathLike,
    file_name: str,
):
    sheets = {
        'sheet1': 0,
        'sheet2': 2,
        'sheet3': 1,
    }
    ss = streamsheet.SessionSheet(
        file_name,
        service_account_json,
        **sheets,
    )
    sheet_name = st.selectbox(
        'Where do you want to write', [
            k for k in sheets.keys()
        ]
    )
    with st.expander(
        f'{sheet_name} selected',
        expanded=True
    ):
        q1 = st.selectbox(
            'What do you want to write', [
                'hello',
                'world',
            ]
        )
        q2 = st.text_input(
            'What do you want to write',
            value='nothing'
        )
        data = {'q1': q1, 'q2': q2}
        clicked = st.button('write')
        if clicked:
            streamsheet.write_json(
                ss.get_worksheet(sheet_name),
                timezone='Asia/Seoul',
                **data
            )
            st.write('✅')
        # NOTE: This is also possible
        # clicked = st.button(
        #     'write',
        #     on_click=streamsheet.callback_write_json(
        #         ss.get_worksheet(sheet_name),
        #         timezone='Asia/Seoul',
        #         **data
        #     )
        # )


if __name__ == '__main__':
    example(
        'service-account.json',
        'example-sheet'
    )
