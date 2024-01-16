import streamlit as st
from components.graph import generateGraph

from components.list import companyList, getPostCount
from scrapperapi import getCompanys, getInsights, getPrompt
from server import generateReportFromCompanyData


def get(key):
    if key in st.session_state:
        return st.session_state[key]
    return None


def set(key, value):
    st.session_state[key] = value


def handle_generate(*, companyId=0, limit=0, offset=0, newPrompt=None):
    report = getInsights(
        companyId=companyId, limit=limit, offset=offset, newPrompt=newPrompt
    )
    st.session_state["response"] = report


st.set_page_config(layout="wide")
st.session_state["basePrompt"] = getPrompt()
# LEFT SIDE
side, content = st.columns([10, 10], gap="medium")
selectedCompany = getCompanys(side)
set("company", selectedCompany)
side.write(f"Total Posts: {selectedCompany.postCount}")
limit, offset = side.columns([5, 5])
limit.number_input(label="Limit", min_value=5, max_value=20, value=10, key="limit")
offset.number_input(label="Offset", min_value=0, value=0, key="offset")
side.text_area(
    label="Prompt", value=st.session_state.basePrompt, height=200, key="basePrompt"
)
side.button(
    label="Generate",
    on_click=lambda: handle_generate(
        companyId=get("company").ID,
        limit=get("limit"),
        offset=get("offset"),
        newPrompt=get("basePrompt"),
    ),
    use_container_width=True,
)

# RIGHT SIDE
content.header("Analysis Report")
content.text(f"Company: {get('company').Name}")
content.divider()
if "response" in st.session_state:
    content.write(st.session_state["response"])
