"""Utility functions for the Streamlit apps.

TODO(bfortuner): Add S3 support.
"""
import json
import os
import re
import shutil
import time
from typing import Any, List, Dict
import uuid

import streamlit as st
from stqdm import stqdm


def inject_inputs(
    prompt_template: str, input_keys: List[str], inputs: Dict[str, Any]
) -> str:
    text = prompt_template
    for field_name, field_value in inputs.items():
        pattern = re.compile("{{" + field_name + "}}", re.IGNORECASE)
        text = pattern.sub(str(inputs[field_name]), text)
    return text


def init_page_layout():
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        .appview-container .main .block-container{
            padding-top: 2rem;    
        }
        .appview-container .css-1adrfps {
            padding-top: 1rem;    
        }
        .appview-container .css-1oe6wy4 {
            padding-top: 1rem;    
        }
        .cell-wrap-text {
            white-space: normal !important;
            font-size: 24px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def make_prompt_id(prompt_name: str):
    return f"{prompt_name}_{str(uuid.uuid1())[:8]}"


def sleep_and_return(st_container, time_per_step, num_steps):
    with st_container:
        for _ in stqdm(range(num_steps)):
            time.sleep(time_per_step)


def init_session_state(widget_keys: List[str], query_params: dict):
    for key in widget_keys:
        if query_params.get(key) is not None:
            query_value = query_params[key][0]
            if key not in st.session_state:
                if "bool" in key:
                    query_value = True if query_value.lower() == "true" else False
                st.session_state[key] = query_value


def write_query_params(widget_values: Dict[str, str]):
    query_params = {}
    for widget_name, widget_value in widget_values.items():
        session_value = st.session_state.get(widget_name)
        if "bool" in widget_name and widget_value is False:
            query_value = session_value if session_value is not None else widget_value
        else:
            query_value = widget_value if widget_value is not None else session_value
        if query_value is not None:
            query_params[widget_name] = query_value

    st.experimental_set_query_params(**query_params)
