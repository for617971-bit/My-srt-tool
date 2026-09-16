            st.download_button(
                label="📥 SRT File Download ဆွဲမည်",
                data=srt_output,
                file_name="chinese_subtitle.srt",
                mime="text/plain"
            )
import os
import sys
import subprocess
import streamlit as st

# ImageMagick & FFmpeg Auto Installer for Streamlit Cloud
st.title("🎬 Subtitle Generator (Chinese to Burmese)")

@st.cache_resource
def install_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        st.warning("FFmpeg ကို စနစ်ထဲ ထည့်သွင်းနေပါသည်... ခဏစောင့်ပေးပါ။")
        os.system("apt-get update && apt-get install -y ffmpeg")

install_ffmpeg()

import whisper

st.write("ဗီဒီယိုဖိုင် တင်ပြီး SRT စာတန်းထိုး ထုတ်ယူနိုင်ပါပြီ။")

uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင် ရွေးပါ", type=["mp4", "mkv", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    if st.button("🚀 SRT စာတန်းထိုး စတင်ထုတ်ယူမည်"):
        with st.spinner("အသံကို စာသားပြောင်းနေပါသည်... (ခဏစောင့်ပေးပါ)"):
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.read())
            
            model = whisper.load_model("base")
            result = model.transcribe("temp_video.mp4")
            
            srt_content = ""
            for i, segment in enumerate(result['segments'], start=1):
                start = segment['start']
                end = segment['end']
                text = segment['text']
                
                def format_time(seconds):
                    hrs = int(seconds // 3600)
                    mins = int((seconds % 3600) // 60)
                    secs = int(seconds % 60)
                    msecs = int((seconds - int(seconds)) * 1000)
                    return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"
                
                srt_content += f"{i}\n{format_time(start)} --> {format_time(end)}\n{text.strip()}\n\n"
            
            st.success("စာတန်းထိုး ထုတ်ယူမှု အောင်မြင်ပါသည်။")
            st.download_button("📥 SRT ဖိုင် ဒေါင်းလုဒ်ဆွဲရန်", srt_content, file_name="subtitles.srt", mime="text/plain")
