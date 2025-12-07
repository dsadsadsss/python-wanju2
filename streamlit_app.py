import os
import streamlit as st
import streamlit.components.v1 as components

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
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1;
        }
        
        /* 视频信息覆盖层 */
        .video-info-overlay {
            position: fixed;
            bottom: 80px;
            left: 20px;
            background: rgba(0, 0, 0, 0.6);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 999;
            font-size: 16px;
            font-weight: bold;
        }
        
        /* 退出按钮 */
        .exit-fullscreen-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.9);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            z-index: 999;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
                st.video(video_bytes)
        except Exception as e:
            st.error(f"加载视频错误: {e}")
    
    # 添加滑动手势检测
    swipe_html = f"""
    <div id="swipe-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 998;"></div>
    <button id="exit-btn" class="exit-fullscreen-btn" onclick="exitFullscreen()">✕</button>
    
    <script>
        let touchStartY = 0;
        let touchEndY = 0;
        const minSwipeDistance = 50;
        
        const container = document.getElementById('swipe-container');
        
        container.addEventListener('touchstart', function(e) {{
            touchStartY = e.touches[0].clientY;
        }}, false);
        
        container.addEventListener('touchmove', function(e) {{
            // 阻止默认滚动行为
            e.preventDefault();
        }}, {{ passive: false }});
        
        container.addEventListener('touchend', function(e) {{
            touchEndY = e.changedTouches[0].clientY;
            handleSwipe();
        }}, false);
        
        function handleSwipe() {{
            const swipeDistance = touchStartY - touchEndY;
            
            if (Math.abs(swipeDistance) > minSwipeDistance) {{
                if (swipeDistance > 0) {{
                    // 向上滑 - 下一个视频
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'next'}}, '*');
                }} else {{
                    // 向下滑 - 上一个视频
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'prev'}}, '*');
                }}
            }}
        }}
        
        function exitFullscreen() {{
            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'exit'}}, '*');
        }}
    </script>
    """
    
    swipe_result = components.html(swipe_html, height=0)
    
    if swipe_result == 'next':
        play_next_video()
        st.rerun()
    elif swipe_result == 'prev':
        play_previous_video()
        st.rerun()
    elif swipe_result == 'exit':
        toggle_fullscreen()
        st.rerun()

# ========== 普通模式 ==========
else:
    st.title("🎬 视频播放器")
    
    st.write(f"**{video_name}**")
    
    # 创建横向按钮布局 - 左右排列
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        st.button("⬅️", key="prev", on_click=play_previous_video, width="stretch", help="上一个")
    
    with col2:
        st.button("➡️", key="next", on_click=play_next_video, width="stretch", help="下一个")
    
    with col3:
        if st.button("🔄", key="reload", width="stretch", help="重新播放"):
            st.rerun()
    
    with col4:
        st.button("⛶", key="fullscreen", on_click=toggle_fullscreen, width="stretch", help="全屏")
    
    # Display current video
    if os.path.exists(video_path):
        try:
            video_bytes = get_video_bytes(current_index)
            if video_bytes:
                st.video(video_bytes)
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
        st.image(image_path, width="stretch")
    
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
        }
        
        .stExpander {
            background-color: rgba(0, 0, 0, 0.02);
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
