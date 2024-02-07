import streamlit as st
from zhipuai import ZhipuAI
import random
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

st.set_page_config(layout="wide")

st.title('Multi LLMs Chat for Virtual Breast Patient')

info_placeholder = st.empty()

case_description = '''
姓名：王淑芬
性别：女
年龄：32岁
主诉：左乳房红肿、疼痛1周，伴发热2天
现病史：1周前开始感觉左侧乳房疼痛，逐渐加重，伴低热。因哺乳中,未服药。2天来寒战、高热，左乳明显红、肿、热、痛，不敢触摸，并伴有局部波动感
生育史：4周前顺利分娩1男婴，母乳喂养中
查体：T39.4度，心率98次/分，呼吸22次/分，血压130/80mmHg。神志清楚，痛苦面容，发育、营养良好，心脏、肺部、腹部查体未见异常。
乳房：左侧乳房肿痛，发热，以内上方为主，明显压痛，范围约8cm*6cm，边界不清，中心部位皮肤呈暗红色，波动感阳性，左侧腋窝可触及2枚肿大淋巴结，约1.5cm*1cm大小,有压痛
实验室检查：血红蛋白128g/L，白细胞26.9，中性粒细胞0.86，血小板155
'''
system_msg =f"""你是一名乳房疾病的患者，在线在乳腺外科门诊诊室中与医生进行谈话。在接下来的对话中，请遵循以下要求：1、请回答用户的提出的疾病相关的问题，不要回答跟问题无关的事情；2、请拒绝回答用户提出的非疾病问题；3、不要回答对疾病对诊断和治疗的其他相关信息。下面是你的特征：
{case_description}
"""
st.info(system_msg)

inquiry = st.chat_input()

LLMS = ['ZhipuAI', 'Qwen', 'BaiChuan']

chat_cols = st.columns(len(LLMS))


for llm in LLMS:
    if llm not in st.session_state:
        st.session_state[llm] = [{'role': 'system', 'content': system_msg},{'role': 'assistant', 'content': '大夫，我乳房不舒服'}]

for index, chat_col in enumerate(chat_cols):
    with chat_col:
        with st.container(height=440, border=True):
            llm = LLMS[index]
            for message in st.session_state[llm]:
                if message['role'] != 'system':
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

info_placeholder.write(st.session_state['Qwen'])

def zhipuai_chat(messages):
    client = ZhipuAI(api_key=st.secrets['zhipuai'])
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
    )
    return {'role': 'assistant', 'content': response.choices[0].message.content}

def qwen_chat(messages):
    response = Generation.call(
        model='qwen-1.8b-chat',
        # messages=messages,
        messages = [
        {'role': 'user', 'content': '用萝卜、土豆、茄子做饭，给我个菜谱'}],
        seed=random.randint(1, 10000),
        result_format='message'
        )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message
    else:
        return response.output.choices[0].message

if inquiry:
    for llm in LLMS:
        st.session_state[llm].append({'role': 'user', 'content': inquiry})
        if llm=='ZhipuAI':
            response = zhipuai_chat(st.session_state[llm])
            st.session_state[llm].append(response)
        if llm=='Qwen':
            st.info(st.session_state[llm])
            response = qwen_chat(st.session_state[llm])
            st.session_state[llm].append(response)
    st.rerun()