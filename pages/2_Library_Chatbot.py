import streamlit as st
from openai import OpenAI

st.title("국립부경대학교 도서관 챗봇")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "library_messages" not in st.session_state:
    st.session_state.library_messages = []

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    value=st.session_state.api_key
)

if api_key:
    st.session_state.api_key = api_key

library_rule = """
국립부경대학교 도서관 규정 내용

도서관은 자료의 수집, 정리, 보존 및 이용을 통하여 교육과 연구를 지원한다.
도서관장은 도서관 운영에 관한 업무를 총괄한다.
도서관 자료는 학생, 교직원 및 도서관장이 인정하는 사람이 이용할 수 있다.
자료의 대출 권수와 기간은 도서관장이 따로 정할 수 있다.
도서관은 필요에 따라 휴관할 수 있으며, 휴관일은 도서관장이 정한다.
이용자는 대출 자료를 정해진 기간 안에 반납해야 한다.
이용자가 자료를 훼손하거나 분실한 경우 변상해야 한다.
"""

if st.button("Clear"):
    st.session_state.library_messages = []
    st.rerun()

for msg in st.session_state.library_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("도서관 규정에 대해 질문하세요")

if user_input:
    st.session_state.library_messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    if not st.session_state.api_key:
        st.warning("API Key를 입력하세요.")
    else:
        client = OpenAI(api_key=st.session_state.api_key)

        prompt = f"""
너는 국립부경대학교 도서관 규정 안내 챗봇이다.
반드시 아래 규정 내용만 바탕으로 대답해라.
규정에 없는 내용은 '규정에서 확인할 수 없습니다'라고 답해라.

[도서관 규정]
{library_rule}

[사용자 질문]
{user_input}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        answer = response.output_text

        st.session_state.library_messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)
