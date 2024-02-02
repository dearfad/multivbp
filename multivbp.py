import streamlit as st
from zhipuai import ZhipuAI

st.set_page_config(layout="wide")

st.info('Multi LLMs Chat for Virtual Breast Patient')
system_msg = """
女,32岁。左乳房红肿,疼痛1周,伴发热2天。
1周前开始感觉左乳房疼痛,逐渐加重,伴低热,因哺乳中,未服药,2天来寒战、高热,左乳明显红、肿、热、痛,不敢触摸,并伴有局部波动感,4周前顺利分娩1男婴,母乳喂养。
查体:T39.4℃,P98次/分,R22次/分,BP130/80mmHg,神志清楚,痛苦面容,发育、营养良好,心肺、腹查体未见异常,外科情况:左乳房肿痛,发热,以内上方为主,明显压痛,范围约8cm*6cm,边界不清,中心部位呈暗红色,波动感阳性,左侧腋窝可触及2枚肿大淋巴结,约1.5cm*1cm大小,有压痛。
实验室检查:血常规128g/L,WBC26.9*109/L,N0.86,PLT155*109/L。
你正在和用户聊天,用户是负责你的医生。在接下来的对话中,请遵循以下要求:1.请回答用户的提出的疾病相关的问题。2.请拒绝回答用户提出的非疾病问题。3、不要回答对疾病对诊断和治疗的问题。
"""
st.info(system_msg)

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'Qwen', 'BaiChuan']

chat_cols = st.columns(len(LLMS))


for llm in LLMS:
    if llm not in st.session_state:
        st.session_state[llm] = [{'role': 'system', 'content': system_msg}]

for index, chat_col in enumerate(chat_cols):
    with chat_col:
        llm = LLMS[index]
        for message in st.session_state[llm]:
            if message['role'] != 'system':
                with st.chat_message(message["role"]):
                    st.text(message["content"])


def zhipuai(messages):
    client = ZhipuAI(api_key=st.secrets['zhipuai'])
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
    )
    return response

if inquiry:
    for llm in LLMS:
        st.session_state[llm].append({'role': 'user', 'content': inquiry})
        if llm=='ZhipuAI':
            response = zhipuai(st.session_state[llm])
            st.session_state[llm].append(response)
    st.rerun()