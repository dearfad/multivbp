import streamlit as st

st.info('Multi LLMs Chat for Virtual Breast Patient')

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'Qwen', 'BaiChuan']

chat_cols = st.columns(len(LLMS))

for llm in LLMS:
    chat_messages[llm] = st.chat_message('user')

for index, chat_col in enumerate(chat_windows):
    with chat_col:
        with chat_messages[LLMS[index]]('user'):
            st.write(LLMS[index])       