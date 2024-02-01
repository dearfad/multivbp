import streamlit as st

st.info('Multi LLMs Chat for Virtual Breast Patient')

inquiry = st.chat_input()

llms = st.columns(3)

with llms[0]:
    st.write('0')


with llms[1]:
    st.write('1')