import streamlit as st
import base64
from pathlib import Path
import streamlit.components.v1 as components
from backend_processor import process_prompt_to_video

# This gets the directory of the currently running script
SCRIPT_DIR = Path(__file__).parent

if 'video_path' not in st.session_state:
    st.session_state.video_path = None
    
st.set_page_config(page_title="manimAI", page_icon="✨", layout="wide")

# Reduce top margin
st.markdown("""
<style>
.main > div {
    padding-top: 0rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Helpers -----------------
def file_to_data_uri(path: Path, mime: str) -> str:
    b = path.read_bytes()
    s = base64.b64encode(b).decode()
    return f"data:{mime};base64,{s}"

def safe_logo_data_uri(path_str: str):
    p = Path(path_str)
    if p.exists():
        try:
            return file_to_data_uri(p, "image/png")
        except Exception:
            return None
    return None

# ----------------- Assets -----------------
logo_uri = safe_logo_data_uri("logo.png")

# Extended demo data with more videos
demo_data = [
    ("demo_videos/demo1.mp4", "The Sierpinski Triangle", "Watch a single triangle transform into a stunning fractal through repeated removal."),
    ("demo_videos/demo2.mp4", "The Smart Search", "Watch the search zone shrink until the target is found in record time."),
    ("demo_videos/demo3.mp4", "Neural Pathways in Motion", "See data pulse through layers, bringing a network to life."),
    ("demo_videos/demo4.mp4", "Capturing the Space Beneath a curve", "Discover how the area under a rising curve expands as we measure it from the starting point up to a chosen limit."),
    ("demo_videos/demo5.mp4", "Growth Showdown", "Watch steady gains meet exponential growth over 20 years."),
    ("demo_videos/demo6.mp4", "The Dancing Cube", "See how we can make a cube dance."),
    ("demo_videos/demo7.mp4", "The Perfect Arc", "See physics launch a cannonball in a flawless 45° journey."),
    ("demo_videos/demo8.mp4", "Animating a Parabola", "Watch as ManimAI plots the classic parabola y = x², drawing the axes and tracing the curve from x = -3 to x = 3."),
]

# ----------------- Hero Section -----------------
st.markdown(
    """
    <style>
    .hero {
      background: linear-gradient(135deg,#6a11cb 0%,#2575fc 100%);
      color: white;
      border-radius: 30px;
      padding: 60px 40px;
      margin-bottom: 20px;
      margin-top: -40px;
      position: relative;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background:
        radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
      pointer-events: none;
    }
    .hero-content {
      position: relative;
      z-index: 1;
    }
    .title-wrapper {
      display: flex;
      align-items: center;
      gap: 24px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }
    .logo-title-container {
      display: flex;
      align-items: center;
      gap: 20px;
    }
    .hero h1 {
      font-size: 48px;
      margin: 0;
      font-weight: 800;
      line-height: 1.1;
    }
    .hero h1 .ai-text {
      background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
      background-size: 400% 400%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: gradientShift 3s ease infinite;
    }
    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .divider {
      width: 2px;
      height: 40px;
      background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.5), transparent);
      flex-shrink: 0;
    }
    .tagline {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 18px;
      color: #feca57;
      font-weight: 500;
    }
    .hero .desc {
      font-size: 17px;
      line-height: 1.6;
      opacity: 0.95;
      max-width: 65%; /* MODIFIED: Prevent text from overlapping animation */
      margin-top: 8px;
    }
    .hero .desc strong {
      font-weight: 600;
      color: #ffffff;
    }
    .hero .desc .highlight {
      color: #feca57;
      font-weight: 500;
    }
    .simple-logo {
      width: 80px;
      height: 80px;
      background: rgba(255,255,255,0.15);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      font-weight: 800;
      color: white;
      border: 3px solid rgba(255,255,255,0.3);
      position: relative;
      overflow: hidden;
      flex-shrink: 0;
    }
    .simple-logo::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 10%;
      right: 10%;
      height: 3px;
      background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb);
      border-radius: 2px;
      transform: translateY(-50%);
      animation: wave 2s ease-in-out infinite;
    }
    @keyframes wave {
      0%, 100% { transform: translateY(-50%) scaleX(0.8); opacity: 0.6; }
      50% { transform: translateY(-50%) scaleX(1.2); opacity: 1; }
    }

    /* --- NEW: Hero Animation --- */
    .hero-animation-container {
        position: absolute;
        top: 50%;
        right: 5%;
        transform: translateY(-50%);
        width: 200px;
        height: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
        pointer-events: none;
    }
    .shape-morph {
        width: 120px;
        height: 120px;
        background-color: transparent;
        border: 4px solid rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        transition: all 1s ease-in-out;
        animation: morph 8s ease-in-out infinite;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2), 0 0 30px rgba(255, 255, 255, 0.1);
    }
    @keyframes morph {
        0%   { transform: rotate(0deg); border-radius: 50%; }
        25%  { transform: rotate(90deg); border-radius: 50%; }
        50%  { transform: rotate(180deg); border-radius: 20%; }
        75%  { transform: rotate(270deg); border-radius: 20%; }
        100% { transform: rotate(360deg); border-radius: 50%; }
    }
    @media (max-width: 992px) {
        .hero-animation-container {
            display: none; /* Hide animation on smaller screens */
        }
        .hero .desc {
            max-width: 100%; /* Allow text to use full width on mobile */
        }
    }
    @media (max-width: 768px) {
      .title-wrapper {
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
      }
      .divider {
        width: 100px;
        height: 2px;
        background: linear-gradient(to right, rgba(255, 255, 255, 0.5), transparent);
      }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Updated hero section with new layout
hero_content = """
<div class="hero">
  <div class="hero-content">
    <div class="title-wrapper">
      <div class="logo-title-container">
        <div class="simple-logo">
          mAI
        </div>
        <h1>Manim<span class="ai-text">AI</span></h1>
      </div>
      <div class="divider"></div>
      <div class="tagline">
        <span>🚀</span>
        <span>Where Mathematical Innovation Meets Artificial Intelligence</span>
      </div>
    </div>
    <div class="desc">
      <strong>Transform math into magic.</strong> Our AI-powered platform instantly converts your mathematical ideas into stunning <span class="highlight">Manim animations</span>. Just describe in plain language — from <span class="highlight">calculus</span> to <span class="highlight">multidimensional spaces</span> — and watch as AI brings your concepts to life with cinema-quality visualizations that captivate and educate.
    </div>
  </div>
  <div class="hero-animation-container">
    <div class="shape-morph"></div>
  </div>
</div>
"""

st.markdown(hero_content, unsafe_allow_html=True)

# ----------------- Scrollable Demo Section -----------------
css = """
<style>
.scroll-wrap {
  max-height: 600px;
  overflow-y: auto;
  padding-right: 12px;
  scrollbar-width: thin;
  scrollbar-color: #6a11cb #f1f1f1;
}
.scroll-wrap::-webkit-scrollbar {
  width: 8px;
}
.scroll-wrap::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
.scroll-wrap::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  border-radius: 10px;
}
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px,1fr));
  gap: 20px;
  padding: 8px 4px 28px 4px;
}
.card {
  background: #f9f9fb;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 24px rgba(20,20,30,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(106, 17, 203, 0.1);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(106, 17, 203, 0.15);
}
.card video { 
  width: 100%; 
  height: 200px; 
  object-fit: cover; 
  border-radius: 8px; 
  background: #000;
  margin-bottom: 12px;
}
.card .caption { 
  font-weight: 600; 
  color: #222; 
  text-align: center;
  font-size: 16px;
  margin-bottom: 8px;
}
.card .description { 
  font-size: 13px; 
  color: #666; 
  text-align: center;
  line-height: 1.4;
}
.demo-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  margin-top: 6px;
}
.demo-count {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}
</style>
"""

cards_html = ""
for src, caption, description in demo_data:
    if src.startswith("http"):
        video_src = src
    else:
        # This builds the full, correct path that works everywhere
        video_file_path = SCRIPT_DIR / src
        video_src = file_to_data_uri(video_file_path, "video/mp4") if video_file_path.exists() else ""

    video_tag = (
        f'<video controls preload="metadata" playsinline>'
        f'<source src="{video_src}" type="video/mp4">Your browser does not support video.</video>'
        if video_src
        else '<div style="height:200px; display:flex; align-items:center; justify-content:center; color:#777; background:#000; border-radius:8px;">Video unavailable</div>'
    )

    cards_html += f'''
    <div class="card">
      {video_tag}
      <div class="caption">{caption}</div>
      <div class="description">{description}</div>
    </div>
    '''

demo_html = css + f"""
<div class="demo-header">
  <h2 style="margin:0; font-size:24px; color:#333;">🎯 Demo Animations</h2>
  <div class="demo-count">{len(demo_data)} examples</div>
</div>
<div class="scroll-wrap">
  <div class="video-grid">
    {cards_html}
  </div>
</div>
"""

components.html(demo_html, height=700, scrolling=False)

# Enhanced styles for the form section
st.markdown("""
<style>
.section-title {
    font-weight: 700;
    font-size: 20px;
    color: #2575fc;
    margin-bottom: -2px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.prompt-box textarea {
    border: 2px solid #2575fc !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    min-height: 250px !important;
}
.preview-title {
    font-weight: 700;
    font-size: 20px;
    color: #6a11cb;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.stButton > button {
    background: linear-gradient(135deg, #6a11cb, #2575fc) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    height: 50px !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(106, 17, 203, 0.3);
}
.create-section-header {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 30px;
    margin-top: 40px;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
}
.center-container {
    display: flex;
    justify-content: center;
    width: 100%;
}

/* Styling for the dropdown */
div[data-baseweb="select"] > div {
    background: linear-gradient(135deg, #6a11cb, #2575fc) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 4px !important;
    font-weight: 600 !important;
    height: 50px !important; 
}
/* Target the placeholder text specifically to ensure its color is white */
div[data-baseweb="select"] > div > div > div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="center-container">
    <h2 class="create-section-header">🎨 Create Your Animation: From Prompt to Preview 🎬</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-title">💭 Enter your prompt:</div>', unsafe_allow_html=True)
    st.markdown('<div class="prompt-box">', unsafe_allow_html=True)
    prompt = st.text_area(
        "",
        height = 250,
        placeholder = "The more detailed your prompt, the better the result. Describe your animation step-by-step here...",
        label_visibility = "collapsed",
        key = "user_prompt" # imp becoz of the code rerun, it stores the value in it and when the code reches here in next run the value in it get stores to the "prompt" -> this happens for every widget
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Set the columns to have equal width
    action_col1, action_col2 = st.columns(2)

with action_col1:
    quality = st.selectbox(
        'Select Quality', # This label is now correctly hidden.
        ('480p', '720p', '1080p', '2160p'),
        index = None, # This makes it so nothing is selected by default.
        placeholder = "✨Select video quality...",
        label_visibility = "collapsed",
        key = "quality"
    )

    with action_col2:
        if st.button("✨ Render Animation", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt before rendering.")
            elif not quality or quality == '✨ Select Quality': # Check if the placeholder is still selected
                st.warning("Please select a video quality.")
            else:
                try:
                    with st.spinner("🎬 Rendering frames... Stitching the final video."):
                        video_path = process_prompt_to_video(prompt, quality)
                        
                        # Store the successful result in session state to remember it
                        st.session_state.video_path = video_path
                    
                    st.success("🎉 Animation rendered successfully!")

                except Exception as e:
                    st.error(f"An error occurred during rendering: {e}")
            

with col2:
    st.markdown('<div class="preview-title">📽️ Animation Preview</div>', unsafe_allow_html=True)
    if st.session_state.video_path:
        st.video(str(st.session_state.video_path))
        st.download_button(
            "⬇️ Download Video",
            data = st.session_state.video_path.read_bytes(),
            file_name = st.session_state.video_path.name,
            mime = "video/mp4",
            use_container_width = True
        )
    else:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(106, 17, 203, 0.05), rgba(37, 117, 252, 0.05));
            border: 2px dashed #6a11cb;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            color: #666;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        '>
            <div style='font-size: 48px; margin-bottom: 16px;'>🎬</div>
            <div style='font-size: 16px; font-weight: 500;'>Your animation preview will appear here</div>
            <div style='font-size: 14px; margin-top: 8px; opacity: 0.8;'>Enter a prompt and click render to get started</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 20px;'>
    <p>✨ Powered by <strong>Manim</strong> and <strong>AI</strong> | 🚀 Create stunning mathematical visualizations with ease</p>
</div>
""", unsafe_allow_html=True)