import os
import subprocess
import streamlit as st
import threading
import psutil

# Load secrets from Streamlit and set them as environment variables
# 按照格式nes = "xxx"在设置里添加nes,nek,tok,dom四个参数
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
    flag_file = "/tmp/command_executed.flag"
    if not os.path.exists(flag_file):
        if not is_bot_js_running():
            subprocess.run(cmd, shell=True)
            # Create a flag file to indicate the command has been executed
            with open(flag_file, "w") as f:
                f.write("Command executed")

# Start the command in a separate thread
def start_thread():
    if not threading.current_thread().name == "MainThread":
        thread = threading.Thread(target=execute_command)
        thread.start()

start_thread()

st.title("抖音美女欣赏")

# Define the paths of the videos in sequential order
video_paths = ["./meinv.mp4", "./mv1.mp4", "./mv2.mp4"]

# Initialize the index to track the current video
current_index = 0

# Function to display the video
def display_video(video_path):
    st.video(video_path)

# Display the current video based on the current_index

st.write("点击下一个按钮播放下一个视频")

display_video(video_paths[current_index])

# Button to play the next video
if st.button("下一个"):
    # Move to the next video in the list
    current_index = (current_index + 1) % len(video_paths)
    # Clear previous video and display the next one
    st.empty()
    display_video(video_paths[current_index])


image_path = "./mv.jpg"
if os.path.exists(image_path):
    st.image(image_path, caption='林熳', use_column_width=True)
st.write("⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️")
st.write("设置里添加nes,nek,tok,dom四个参数")
st.write("⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️⭐️")
