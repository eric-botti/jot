import json

import streamlit as st

from openai import OpenAI

title = "Jot"

st.set_page_config(title, layout="wide")
st.title(title)


# Initialize OpenAI client
if "client" not in st.session_state:
    st.session_state.client = OpenAI()

st.header("Transform")

templates = json.loads(open("templates.json").read())

template_name = st.radio("Template", templates.keys(), horizontal=True)

st.write(templates[template_name]['description'])

with st.expander("Show Template Format"):
    st.markdown(templates[template_name]['format'])

st.divider()

left, right = st.columns(2)

with left:
    st.header("Record")
    raw_text = st.text_area("Write your notes here")


with right:
    st.header("Result")

    prompt = "\n\n".join(
        [
            "Reformat the provided text to match the format of the following template:",
            # "## Name:",
            # template_name,
            # "## Description:",
            # templates[template_name]['description'],
            # "## Format:",
            templates[template_name]['format']
        ]
    )

    if raw_text:
        # We need a way to match the prompt with the template responses...

        if "responses" not in st.session_state:
            st.session_state.responses = {}

        if template_name not in st.session_state.responses:
            st.session_state.responses[template_name] = st.session_state.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': raw_text}
                ]
            )

        result = st.session_state.responses[template_name].choices[0].message.content

        st.markdown(result)