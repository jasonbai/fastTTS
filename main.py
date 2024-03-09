import streamlit as st
from subprocess import run, PIPE
import tempfile
import os

# 这个列表可以是从`edge-tts --list-voices`的输出手动提取的
voices = [
    {"name": "en-US-AndrewNeural - Female", "shortname": "en-US-AndrewNeural"},
    {"name": "zh-CN-XiaoxiaoNeural - Female", "shortname": "zh-CN-XiaoxiaoNeural"},
    # 添加更多可用的语音...
]

# 设置Streamlit页面
st.title('TTS语音生成器')
st.header('请在下方输入你想转换为语音的文本：')

# 选择语音
voice_options = {voice["name"]: voice["shortname"] for voice in voices}
selected_voice = st.selectbox("选择语音", options=list(voice_options.keys()))

# 用户输入文本
user_input = st.text_area("文本输入", "Hey there, welcome to this tool! It's here to help you get your text converted into spoken words.")

# 处理用户点击事件
if st.button('生成音频'):
    # 使用临时文件来安全地处理文件操作
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        filepath = tmpfile.name

    # 构建并执行命令
    voice_shortname = voice_options[selected_voice]
    command = ['edge-tts', '--voice', voice_shortname, '--text', f'"{user_input}"', '--write-media', filepath]
    process = run(' '.join(command), shell=True, stdout=PIPE, stderr=PIPE)

    # 如果生成成功，提供下载链接
    if process.returncode == 0:
        with open(filepath, "rb") as file:
            st.download_button(label="下载音频文件", data=file, file_name="tts_audio.mp3", mime="audio/mpeg")
        st.success("音频生成成功！")
    else:
        st.error("音频生成失败，请检查你的输入。")

    # 清理临时文件
    os.unlink(filepath)
