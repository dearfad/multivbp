import streamlit as st

st.info('Multi LLMs Chat for Virtual Breast Patient')

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'qwen']

chat_windows = st.columns(len(LLMS))

for index, chat_window in enumerate(chat_windows):
    with chat_window:
        st.write(LLMS[index])