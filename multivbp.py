import streamlit as st

st.info('Multi LLMs Chat for Virtual Breast Patient')

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'Qwen', 'BaiChuan']

chat_cols = st.columns(len(LLMS))

for index, chat_col in enumerate(chat_cols):
    with chat_col:
        with chat_messages('user'):
            st.write(LLMS[index])       