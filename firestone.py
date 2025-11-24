import streamlit as st
import os
from openai import OpenAI



client = OpenAI(
    api_key= st.secrets['HunYuan_API_KEY'],
    base_url="https://api.hunyuan.cloud.tencent.com/v1")

def judge_level(text):
    response = client.chat.completions.create(
        model="hunyuan-turbos-latest",
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": text},
        ],
        temperature= 0.7
    )
    return response, response.choices[0].message.content

def tiao_zheng(text):
    response = client.chat.completions.create(
        model="hunyuan-turbos-latest",
        messages=[
            {"role": "system", "content": "### 定位：语言表述专家\n ### 任务：将歧视性语句换一种方法表述，使表述中不包含歧视语义。"},
            {"role": "user", "content": text},
        ],
        temperature= 0.7
    )
    return response, response.choices[0].message.content



st.title('💩💩💩语言检测及纠正')
st.set_page_config(page_title='我的第一个')
user_input = st.text_area('请输入要发言的句子：',height=100)

if st.button('开始分析'):
    st.spinner('正在分析中')
    if user_input.strip() == '':
        st.warning('请输入文本')
    else:
        # try:
        score = judge_level(user_input)
        score = score[1]
        st.success(f'歧视分析结果得分：{score}')
        if score != '1':
            st.spinner("请稍等")
            result = tiao_zheng(user_input)
            result = result[1].split('\n\n')[0]
            st.success(f'调整后的语句是：{result}')


