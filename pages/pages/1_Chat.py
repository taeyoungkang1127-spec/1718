import streamlit as st
from openai import OpenAI

st.title("Chat 페이지")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    value=st.session_state.api_key
)

if api_key:
    st.session_state.api_key = api_key

if st.button("Clear"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    if not st.session_state.api_key:
        st.warning("API Key를 입력하세요.")
    else:
        client = OpenAI(api_key=st.session_state.api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=st.session_state.messages
        )

        assistant_reply = response.output_text

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        with st.chat_message("assistant"):
            st.write(assistant_reply)
