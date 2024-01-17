import streamlit as st
from components.list import companyList
from scrapperapi import getCompanys, getInsights, getPrompt
from tools import getDownloadURI, prepareResponse


def get(key):
    if key in st.session_state:
        value = st.session_state[key]

        # Check if the value is a streamlit element
        if isinstance(value, st.delta_generator.DeltaGenerator):
            # If it's a text_area, extract the value
            if value.dg_type == "text_area":
                return value.new_element.widget.value

        return value

    return None


def set(key, value):
    st.session_state[key] = value


def handle_generate(*, companyId=0, limit=0, offset=0, newPrompt=None):
    if "response" in st.session_state:
        del st.session_state["response"]
    report = getInsights(
        companyId=companyId, limit=limit, offset=offset, newPrompt=newPrompt
    )
    st.session_state["response"] = report


st.set_page_config(layout="wide")

# LEFT SIDE
side, content = st.columns([10, 10], gap="medium")
selectedCompany = companyList(side)
set("company", selectedCompany)
side.write(f"Total Posts: {selectedCompany.postCount}")
limit, offset = side.columns([5, 5])
limit.number_input(label="Limit", min_value=5, max_value=20, value=10, key="limit")
offset.number_input(label="Offset", min_value=0, value=0, key="offset")

# Use st.text_area directly and set the value in the session state
side.text_area(
    label="Prompt",
    height=200,
    value=getPrompt()["prompt"],
    key="basePrompt",
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
contenttitle, downloadbutton = content.columns([7, 3])
contenttitle.header("Analysis Report")
downloadbutton.markdown("")

if "response" in st.session_state:
    downloadbutton.link_button(
        label="Download PDF",
        url=getDownloadURI(prepareResponse(st)),
    )

content.markdown(f"Company: **{get('company').Name}**")
content.divider()

if "response" in st.session_state:
    content.write(st.session_state["response"])
