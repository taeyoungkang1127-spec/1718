import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.title("ChatPDF 페이지")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []

api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    value=st.session_state.api_key
)

if api_key:
    st.session_state.api_key = api_key

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

@st.cache_data
def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

if uploaded_file is not None:
    st.session_state.pdf_text = read_pdf(uploaded_file)
    st.success("PDF 업로드 완료!")

if st.button("Clear"):
    st.session_state.pdf_text = ""
    st.session_state.pdf_messages = []
    st.rerun()

for msg in st.session_state.pdf_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("PDF 내용에 대해 질문하세요")

if user_input:
    st.session_state.pdf_messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    if not st.session_state.api_key:
        st.warning("API Key를 입력하세요.")
    elif not st.session_state.pdf_text:
        st.warning("PDF를 먼저 업로드하세요.")
    else:
        client = OpenAI(api_key=st.session_state.api_key)

        prompt = f"""
너는 PDF 내용을 바탕으로 답변하는 챗봇이다.
반드시 아래 PDF 내용만 참고해서 대답해라.
PDF에 없는 내용은 'PDF에서 확인할 수 없습니다'라고 답해라.

[PDF 내용]
{st.session_state.pdf_text[:12000]}

[사용자 질문]
{user_input}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        answer = response.output_text

        st.session_state.pdf_messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)
