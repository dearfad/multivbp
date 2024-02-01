import streamlit as st

st.info('Multi LLMs Chat for Virtual Breast Patient')

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'Qwen', 'BaiChuan']

chat_cols = st.columns(len(LLMS))

for llm in LLMS:
    if llm not in st.session_state:
        st.session_state[llm] = []

for index, chat_col in enumerate(chat_cols):
    with chat_col:
        llm = LLMS[index]
        with st.chat_message('user'):
            st.write(llm)   
            st.write(st.session_state[llm])