import os
import streamlit as st
import base64

st.set_page_config(page_title="Video Player", page_icon="🎬", layout="wide")

# 初始化全屏状态
if 'fullscreen' not in st.session_state:
    st.session_state['fullscreen'] = False

# Get all mp4 files from ./mp4/ folder
video_folder = "./mp4/"

# Check if folder exists
if not os.path.exists(video_folder):
    st.error(f"视频文件夹 '{video_folder}' 未找到。请创建文件夹并添加 MP4 文件。")
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

# Initialize session state for current video index
if 'playing_index' not in st.session_state:
    st.session_state['playing_index'] = 0

# Initialize preloaded videos cache
if 'video_cache' not in st.session_state:
    st.session_state['video_cache'] = {}

# Ensure index is within bounds
st.session_state['playing_index'] = st.session_state['playing_index'] % len(video_files)

# Function to load video into cache
def load_video_to_cache(index):
    """预加载视频到缓存"""
    if index < 0 or index >= len(video_files):
        return
    
    video_file = video_files[index]
    if video_file not in st.session_state['video_cache']:
        video_path = os.path.join(video_folder, video_file)
        try:
            with open(video_path, 'rb') as f:
                st.session_state['video_cache'][video_file] = f.read()
        except Exception as e:
            pass

# Function to get video from cache or load it
def get_video_bytes(index):
    """从缓存获取视频，如果没有则加载"""
    video_file = video_files[index]
    if video_file not in st.session_state['video_cache']:
        load_video_to_cache(index)
    return st.session_state['video_cache'].get(video_file)

# Navigation functions
def play_previous_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] - 1) % len(video_files)
    preload_adjacent_videos()

def play_next_video():
    st.session_state['playing_index'] = (st.session_state['playing_index'] + 1) % len(video_files)
    preload_adjacent_videos()

def toggle_fullscreen():
    st.session_state['fullscreen'] = not st.session_state['fullscreen']

def preload_adjacent_videos():
    """预加载相邻的视频"""
    current_index = st.session_state['playing_index']
    
    # 预加载下一个视频
    next_index = (current_index + 1) % len(video_files)
    load_video_to_cache(next_index)
    
    # 预加载上一个视频
    prev_index = (current_index - 1) % len(video_files)
    load_video_to_cache(prev_index)
    
    # 可选：预加载下下个视频（提前两个）
    next_next_index = (current_index + 2) % len(video_files)
    load_video_to_cache(next_next_index)

# 初始加载：预加载当前和相邻视频
current_index = st.session_state['playing_index']
load_video_to_cache(current_index)
preload_adjacent_videos()

# 获取当前视频信息
current_video = video_files[current_index]
video_name = os.path.splitext(current_video)[0]
video_path = os.path.join(video_folder, current_video)

# ========== 全屏模式 ==========
if st.session_state['fullscreen']:
    # 全屏模式：只显示视频和滑动按钮
    st.markdown("""
    <style>
        /* 隐藏 Streamlit 默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 全屏容器 */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
        }
        
        /* 视频全屏样式 */
        [data-testid="stVideo"] {
            width: 100% !important;
            height: 85vh !important;
            border-radius: 0px;
        }
        
        /* 滑动按钮容器 */
        .fullscreen-controls {
            position: fixed;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        /* 滑动按钮样式 */
        .swipe-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.9);
            border: none;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        
        .swipe-button:hover {
            background: rgba(255, 255, 255, 1);
            transform: scale(1.1);
        }
        
        /* 退出按钮 */
        .exit-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(255, 100, 100, 0.9);
            border: none;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        /* 视频信息覆盖层 */
        .video-info-overlay {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            z-index: 999;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 视频信息覆盖层
    st.markdown(f"""
    <div class="video-info-overlay">
        <div style="font-size: 18px; font-weight: bold;">{video_name}</div>
        <div style="font-size: 14px; opacity: 0.8;">视频 {current_index + 1} / {len(video_files)}</div>
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
    
    # 创建侧边滑动控制按钮
    col1, col2, col3 = st.columns([8, 1, 1])
    
    with col2:
        st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
        if st.button("🔼", key="swipe_up_fs", help="上一个视频"):
            play_previous_video()
            st.rerun()
        
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        if st.button("🔽", key="swipe_down_fs", help="下一个视频"):
            play_next_video()
            st.rerun()
        
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        if st.button("❌", key="exit_fs", help="退出全屏"):
            toggle_fullscreen()
            st.rerun()

# ========== 普通模式 ==========
else:
    st.title("🎬 视频播放器")
    
    # 显示当前视频信息和缓存状态
    col_info1, col_info2 = st.columns([3, 1])
    with col_info1:
        st.write(f"**正在播放:** {video_name}")
        st.caption(f"视频 {current_index + 1} / {len(video_files)}")
    with col_info2:
        cached_count = len(st.session_state['video_cache'])
        st.caption(f"📦 已缓存: {cached_count}/{len(video_files)}")
    
    # 创建横向按钮布局
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col1:
        st.button("⬅️ 上一个", on_click=play_previous_video, width="stretch")
    
    with col2:
        st.button("🔼 向上滑", on_click=play_previous_video, width="stretch")
    
    with col3:
        st.button("🔽 向下滑", on_click=play_next_video, width="stretch")
    
    with col4:
        st.button("下一个 ➡️", on_click=play_next_video, width="stretch")
    
    with col5:
        if st.button("🔄 重新播放"):
            st.rerun()
    
    with col6:
        st.button("⛶ 全屏", on_click=toggle_fullscreen, width="stretch")
    
    # Display current video from cache
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
    
    # 添加预加载状态指示
    with st.expander("⚡ 预加载状态"):
        st.write("**已预加载的视频:**")
        for idx, video in enumerate(video_files):
            video_status = "✅" if video in st.session_state['video_cache'] else "⬜"
            current_marker = "▶️" if idx == current_index else ""
            st.text(f"{video_status} {current_marker} {os.path.splitext(video)[0]}")
    
    # 添加缓存管理按钮
    col_cache1, col_cache2 = st.columns(2)
    with col_cache1:
        if st.button("🚀 预加载所有视频"):
            with st.spinner("正在预加载所有视频..."):
                for idx in range(len(video_files)):
                    load_video_to_cache(idx)
            st.success(f"已预加载 {len(video_files)} 个视频！")
            st.rerun()
    
    with col_cache2:
        if st.button("🗑️ 清除缓存"):
            st.session_state['video_cache'] = {}
            st.success("缓存已清除！")
            st.rerun()
    
    # 添加键盘快捷键提示
    st.divider()
    st.caption("💡 提示：点击 🔼 向上滑 或 🔽 向下滑 来切换视频")
    st.caption("⚡ 预加载功能：自动预加载相邻3个视频，实现无缝切换")
    st.caption("⛶ 全屏模式：沉浸式观看体验，只显示视频和滑动控制")
    
    # Optional: Display playlist
    with st.expander("📋 播放列表"):
        for idx, video in enumerate(video_files):
            cached_indicator = "✅" if video in st.session_state['video_cache'] else ""
            if idx == st.session_state['playing_index']:
                st.write(f"▶️ **{os.path.splitext(video)[0]}** {cached_indicator}")
            else:
                if st.button(f"▷ {os.path.splitext(video)[0]} {cached_indicator}", key=f"video_{idx}"):
                    st.session_state['playing_index'] = idx
                    preload_adjacent_videos()
                    st.rerun()
    
    # Optional: Display image
    image_path = "./mv.jpg"
    if os.path.exists(image_path):
        st.divider()
        st.image(image_path, width="stretch")
    
    # 添加自定义CSS来增强体验
    st.markdown("""
    <style>
        /* 让视频容器更突出 */
        [data-testid="stVideo"] {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* 按钮样式优化 */
        .stButton button {
            font-weight: 500;
        }
        
        /* 缓存状态样式 */
        .stExpander {
            background-color: rgba(0, 0, 0, 0.02);
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
