import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="LLM Web App", page_icon="🤖")

st.title("LLM 응답 웹 앱")

st.write("OpenAI API Key를 입력하고 질문을 하면 AI가 답변합니다.")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    value=st.session_state.api_key
)

if api_key:
    st.session_state.api_key = api_key

question = st.text_area("질문을 입력하세요")

@st.cache_data
def get_llm_response(api_key, question):
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=question
    )

    return response.output_text

if st.button("응답 받기"):
    if not st.session_state.api_key:
        st.warning("API Key를 먼저 입력하세요.")
    elif not question:
        st.warning("질문을 입력하세요.")
    else:
        answer = get_llm_response(st.session_state.api_key, question)
        st.subheader("AI 응답")
        st.write(answer)
