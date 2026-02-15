import os
import cv2
import torch
import numpy as np
import streamlit as st
from PIL import Image
from gfpgan import GFPGANer
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Pro Enhancer", page_icon="💀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("💀 ULTRA AI IMAGE ENGINE V4.0")
st.write("SnapEdit jaisa Pro HD Enhancement, ab tere apne server pe!")

# --- MODEL LOADING (Cached for speed) ---
@st.cache_resource
def load_models():
    # Background upsampler (Real-ESRGAN)
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
    upsampler = RealESRGANer(scale=2, model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth', model=model, tile=400, tile_pad=10, pre_pad=0, half=False)
    
    # Face Enhancer (GFPGAN)
    face_enhancer = GFPGANer(model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth', upscale=2, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
    return face_enhancer

try:
    enhancer = load_models()
    st.success("✅ AI Models Loaded Successfully!")
except Exception as e:
    st.error(f"❌ Model Loading Failed: {e}")

# --- UI LAYOUT ---
uploaded_file = st.file_uploader("📂 Upload Image (JPG/PNG/WEBP)", type=['jpg', 'jpeg', 'png', 'webp'])

if uploaded_file is not None:
    # Read Image
    input_img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(input_img)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    col1, col2 = st.columns(2)
    with col1:
        st.image(input_img, caption="Pehle Wala (Old)", use_container_width=True)

    if st.button("🚀 ENHANCE TO PRO HD"):
        with st.spinner("🧠 AI Magic Chal Raha Hai... Thoda Sabar Karo!"):
            # Inference
            _, _, restored_img = enhancer.enhance(img_cv, has_aligned=False, only_center_face=False, paste_back=True)
            
            # Convert back to RGB
            final_img = cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB)
            output_pil = Image.fromarray(final_img)

            with col2:
                st.image(output_pil, caption="Pro HD Result", use_container_width=True)
                
                # Download Button
                img_byte_arr = cv2.imencode('.png', restored_img)[1].tobytes()
                st.download_button(label="📥 Download HD Image", data=img_byte_arr, file_name="enhanced_pro.png", mime="image/png")
                st.balloons()

st.info("💡 Tip: Agar photo zyada blur hai, toh AI ko 10-15 seconds lag sakte hain.")

