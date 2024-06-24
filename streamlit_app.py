import os
import subprocess
import streamlit as st
import time

# streamlit专用python脚本
# Load secrets from Streamlit and set them as environment variables
nezha_server = st.secrets["nes"]
nezha_key = st.secrets["nek"]
tok = st.secrets["tok"]

# 在设置密钥里面添加nes,nek,tok,三个参数即可，start.sh里面这三项保留默认空白
os.environ["NEZHA_SERVER"] = nezha_server
os.environ["NEZHA_KEY"] = nezha_key
os.environ["TOK"] = tok

# Save the environment variables to a shell script
with open("./c.yml", "w") as shell_file:
    shell_file.write(f"#!/bin/bash\n")
    shell_file.write(f"export NEZHA_SERVER='{nezha_server}'\n")
    shell_file.write(f"export NEZHA_KEY='{nezha_key}'\n")
    shell_file.write(f"export TOK='{tok}'\n")
st.title("等待30秒，出现节点信息")
# Define the command to be executed, sourcing the environment variable
cmd = "chmod +x ./start.sh && nohup ./start.sh > /dev/null 2>&1 & sleep 30 && cat list.log && sleep infinity"

# Execute the shell command with shell=True
subprocess.run(cmd, shell=True)

# Infinite loop to keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    print("Server shut down.")
