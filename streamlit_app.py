import os
import subprocess
from flask import Flask
from multiprocessing import Process
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
    shell_file.write(f"export NEZHA_SERVER='{nezha_server}'\n")
    shell_file.write(f"export NEZHA_KEY='{nezha_key}'\n")
    shell_file.write(f"export TOK='{tok}'\n")

# Function to start the web server
def start_server(port):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    app.run(host='0.0.0.0', port=port)

# Set default port to 8080 or use SERVER_PORT or PORT environment variable
port = int(os.environ.get('SERVER_PORT', os.environ.get('PORT', 8080)))

# Define the command to be executed, sourcing the environment variables first
cmd = "chmod +x ./start.sh && nohup ./start.sh > /dev/null 2>&1 & sleep 9999999999999999999999999999"

# Start the web server in a separate process
server_process = Process(target=start_server, args=(port,))
server_process.start()

# Execute the shell command with shell=True
subprocess.run(cmd, shell=True)

# Infinite loop to keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    server_process.terminate()
    server_process.join()
    print("Server shut down.")
