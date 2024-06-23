import os
import subprocess
from flask import Flask
from multiprocessing import Process
import streamlit as st

# Load secrets from Streamlit and set them as environment variables
nezha_server = st.secrets["nes"]
nezha_key = st.secrets["nek"]
tok = st.secrets["tok"]

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
port = int(os.environ.get('SERVER_PORT', os.environ.get('PORT', 3000)))

# Define the command to be executed, sourcing the environment variables first
cmd = ". ./c.yml && chmod +x ./start.sh && ./start.sh"

# Start the web server in a separate process
server_process = Process(target=start_server, args=(port,))
server_process.start()

# Execute the shell command with shell=True
subprocess.run(cmd, shell=True)

# Optionally, join the server process if you want the script to wait for the server to finish
server_process.join()
