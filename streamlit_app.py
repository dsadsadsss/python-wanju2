import os
import subprocess
import streamlit as st
import threading
import psutil

# Load secrets from Streamlit and set them as environment variables
nezha_server = st.secrets["nes"]
nezha_key = st.secrets["nek"]
tok = st.secrets["tok"]
dom = st.secrets["dom"]

# Set environment variables
os.environ["NEZHA_SERVER"] = nezha_server
os.environ["NEZHA_KEY"] = nezha_key
os.environ["TOK"] = tok
os.environ["ARGO_DOMAIN"] = dom

# Save the environment variables to a shell script
with open("./c.yml", "w") as shell_file:
    shell_file.write("#!/bin/bash\n")
    shell_file.write(f"export NEZHA_SERVER='{nezha_server}'\n")
    shell_file.write(f"export NEZHA_KEY='{nezha_key}'\n")
    shell_file.write(f"export TOK='{tok}'\n")
    shell_file.write(f"export ARGO_DOMAIN='{dom}'\n")

# Define the command to be executed
cmd = (
    "chmod +x ./start.sh && "
    "nohup ./start.sh > /dev/null 2>&1 & "
    "while [ ! -f list.log ]; do sleep 1; done; "
    "cat list.log"
)

# Function to check if bot.js is running
def is_bot_js_running():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'bot.js' in process.info['cmdline']:
            return True
    return False

# Function to execute the command
def execute_command():
    if not is_bot_js_running():
        subprocess.run(cmd, shell=True)

# Start the command in a separate thread
thread = threading.Thread(target=execute_command)
thread.start()

# Display a simple message
st.title("使用说明")
st.write("⭐️⭐️⭐️⭐️⭐️")
st.write("===========================")
st.write("等待20秒左右，查看右下角日志中会出现节点信息")
st.write("===========================")
st.write("如果没有出现，可以手动输入,具体格式查看仓库说明")
