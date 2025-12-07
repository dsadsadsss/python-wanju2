import os
import streamlit as st

st.set_page_config(page_title="Video Player", page_icon="🎬", layout="wide")

# 初始化全屏状态
if 'is_fullscreen' not in st.session_state:
    st.session_state['is_fullscreen'] = False

# Get all mp4 files from ./mp4/ folder
video_folder = "./mp4/"

# Check if folder exists
if not os.path.exists(video_folder):
    st.error(f"视频文件夹 '{video_folder}' 未找到。")
    st.stop()

# Get video files with error handling
try:
    video_files = [f for f in os.listdir(video_folder) if f.lower().endswith('.mp4')]
    video_files.sort()
except Exception as e:
    st.error(f"读取视频文件夹错误: {e}")
    st.stop()

if not video_files:
    st.warning("视频文件夹中没有找到 MP4 文件。")
    st.stop()

# Initialize session state
if 'playing_index' not in st.session_state:
    st.session_state['playing_index'] = 0
if 'video_cache' not in st.session_state:
    st.session_state['video_cache'] = {}

st.session_state['playing_index'] = st.session_state['playing_index'] % len(video_files)

# Function to load video into cache
def load_video_to_cache(index):
    if index < 0 or index >= len(video_files):
        return
    video_file = video_files[index]
    if video_file not in st.session_state['video_cache']:
        video_path = os.path.join(video_folder, video_file)
        try:
            with open(video_path, 'rb') as f:
                st.session_state['video_cache'][video_file] = f.read()
        except:
            pass

def get_video_bytes(index):
    video_file = video_files[index]
    if video_file not in st.session_state['video_cache']:
        load_video_to_cache(index)
    return st.session_state['video_cache'].get(video_file)

def play_previous_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] - 1) % len(video_files)
    preload_adjacent_videos()

def play_next_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] + 1) % len(video_files)
    preload_adjacent_videos()

def toggle_fullscreen():
    st.session_state['is_fullscreen'] = not st.session_state['is_fullscreen']

def preload_adjacent_videos():
    current_index = st.session_state['playing_index']
    next_index = (current_index + 1) % len(video_files)
    load_video_to_cache(next_index)
    prev_index = (current_index - 1) % len(video_files)
    load_video_to_cache(prev_index)
    next_next_index = (current_index + 2) % len(video_files)
    load_video_to_cache(next_next_index)

# 初始加载
current_index = st.session_state['playing_index']
load_video_to_cache(current_index)
preload_adjacent_videos()

# 获取当前视频信息
current_video = video_files[current_index]
video_name = os.path.splitext(current_video)[0]
video_path = os.path.join(video_folder, current_video)

# ========== 全屏模式 ==========
if st.session_state['is_fullscreen']:
    # 全屏模式CSS
    st.markdown("""
    <style>
        /* 隐藏所有Streamlit默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {visibility: hidden;}
        
        /* 全屏容器 */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* 视频全屏样式 */
        [data-testid="stVideo"] {
            width: 100vw !important;
            height: 100vh !important;
            border-radius: 0px;
        }
        
        /* 视频信息覆盖层 */
        .video-info-overlay {
            position: fixed;
            bottom: 100px;
            left: 20px;
            background: rgba(0, 0, 0, 0.6);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 999;
            font-size: 16px;
            font-weight: bold;
        }
        
        /* 控制按钮容器 */
        .fullscreen-controls {
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 999;
            pointer-events: none;
        }
        
        /* 按钮样式 */
        .stButton {
            pointer-events: auto;
        }
        
        .stButton button {
            background: rgba(255, 255, 255, 0.95) !important;
            border: none !important;
            border-radius: 50% !important;
            width: 55px !important;
            height: 55px !important;
            font-size: 22px !important;
            box-shadow: 0 3px 10px rgba(0,0,0,0.4) !important;
            padding: 0 !important;
            min-height: 55px !important;
            color: #333 !important;
        }
        
        .stButton button:hover {
            background: rgba(255, 255, 255, 1) !important;
            transform: scale(1.15);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
        }
        
        /* 列布局优化 */
        [data-testid="column"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 视频信息覆盖层
    st.markdown(f"""
    <div class="video-info-overlay">
        {video_name}
    </div>
    """, unsafe_allow_html=True)
    
    # 显示视频
    if os.path.exists(video_path):
        try:
            video_bytes = get_video_bytes(current_index)
            if video_bytes:
                st.video(video_bytes, autoplay=True)
        except Exception as e:
            st.error(f"加载视频错误: {e}")
    
    # 创建悬浮控制按钮 - 底部居中横向排列
    st.markdown("""
    <div class="fullscreen-controls">
        <div id="btn-container" style="display: flex; gap: 15px; align-items: center;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用列布局创建按钮
    col_spacer1, col_btn1, col_btn2, col_btn3, col_btn4, col_spacer2 = st.columns([2, 1, 1, 1, 1, 2])
    
    with col_btn1:
        if st.button("⬅️", key="fs_prev", use_container_width=True):
            play_previous_video()
            st.rerun()
    
    with col_btn2:
        if st.button("➡️", key="fs_next", use_container_width=True):
            play_next_video()
            st.rerun()
    
    with col_btn3:
        if st.button("🔄", key="fs_reload", use_container_width=True):
            st.rerun()
    
    with col_btn4:
        if st.button("❌", key="fs_exit", use_container_width=True):
            toggle_fullscreen()
            st.rerun()

# ========== 普通模式 ==========
else:
    st.title("❤️ 抖音美女欣赏 ❤️")
    
    st.write(f"**{video_name}**")
    
    # 创建横向按钮布局 - 视频上方排列
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("⬅️", key="prev", on_click=play_previous_video, use_container_width=True, help="上一个")
    
    with col2:
        st.button("➡️", key="next", on_click=play_next_video, use_container_width=True, help="下一个")
    
    with col3:
        if st.button("🔄", key="reload", use_container_width=True, help="重新播放"):
            st.rerun()
    
    with col4:
        st.button("⛶", key="fullscreen", on_click=toggle_fullscreen, use_container_width=True, help="全屏")
    
    # Display current video
    if os.path.exists(video_path):
        try:
            video_bytes = get_video_bytes(current_index)
            if video_bytes:
                st.video(video_bytes, autoplay=True)
            else:
                st.error("视频加载失败")
        except Exception as e:
            st.error(f"加载视频错误: {e}")
    else:
        st.error(f"视频文件未找到: {video_path}")
    
    # 播放列表
    with st.expander("📋 播放列表"):
        for idx, video in enumerate(video_files):
            if idx == st.session_state['playing_index']:
                st.write(f"▶️ **{os.path.splitext(video)[0]}**")
            else:
                if st.button(f"▷ {os.path.splitext(video)[0]}", key=f"video_{idx}"):
                    st.session_state['playing_index'] = idx
                    preload_adjacent_videos()
                    st.rerun()
    
    # 管理功能
    with st.expander("⚙️ 管理"):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("🚀 预加载全部"):
                for idx in range(len(video_files)):
                    load_video_to_cache(idx)
                st.rerun()
        with col_m2:
            if st.button("🗑️ 清除缓存"):
                st.session_state['video_cache'] = {}
                st.rerun()
    
    # Optional: Display image
    image_path = "./mv.jpg"
    if os.path.exists(image_path):
        st.divider()
        st.image(image_path, use_container_width=True)
    
    # 普通模式CSS
    st.markdown("""
    <style>
        [data-testid="stVideo"] {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .stButton button {
            font-weight: 500;
            font-size: 24px;
            height: 60px;
            white-space: nowrap;
        }
        
        /* 确保列在手机上不换行 */
        [data-testid="column"] {
            min-width: 0 !important;
        }
        
        .row-widget {
            flex-wrap: nowrap !important;
        }
        
        .stExpander {
            background-color: rgba(0, 0, 0, 0.02);
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
