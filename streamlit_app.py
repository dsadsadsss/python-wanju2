import os
import subprocess
import streamlit as st
import threading

# Load secrets from Streamlit and set them as environment variables
nezha_server = st.secrets["nes"]
nezha_key = st.secrets["nek"]
tok = st.secrets["tok"]
dom = st.secrets["dom"]

# 在Streamlit创建设置密钥里面添加nes,nek,tok,dom三四个参数即可
# 按照nes = "xxx.eu.org"这样格式添加四个参数值
# start.sh里面这四项保留默认空白，其他参数可以直接在start.sh里面修改
os.environ["NEZHA_SERVER"] = nezha_server
os.environ["NEZHA_KEY"] = nezha_key
os.environ["TOK"] = tok
os.environ["ARGO_DOMAIN"] = dom

# Save the environment variables to a shell script
with open("./c.yml", "w") as shell_file:
    shell_file.write(f"#!/bin/bash\n")
    shell_file.write(f"export NEZHA_SERVER='{nezha_server}'\n")
    shell_file.write(f"export NEZHA_KEY='{nezha_key}'\n")
    shell_file.write(f"export TOK='{tok}'\n")
    shell_file.write(f"export ARGO_DOMAIN='{dom}'\n")

# Define the command to be executed
cmd = "chmod +x ./start.sh && nohup ./start.sh > /dev/null 2>&1 & while [ ! -f list.log ]; do sleep 1; done; tail -f list.log"

# Function to execute the command
def execute_command():
    subprocess.run(cmd, shell=True)

# Start the command in a separate thread
thread = threading.Thread(target=execute_command)
thread.start()

# UI elements
st.title("⭐️⭐️⭐️⭐️⭐️")
st.title("================")
st.title("等待20秒左右，查看右下角日志中会出现节点信息")
st.title("================")
st.title("如果没有出现，可以手动输入,具体格式查看仓库说明")

# Display a simple message
st.write("Hello, World!")
