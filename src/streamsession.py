# Third party
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_session_id():
    ctx = get_script_run_ctx()
    return ctx.session_id
