import streamlit as st
import whisper
import os
import subprocess
from deep_translator import GoogleTranslator

# Ensure FFmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
    st.info("Installing FFmpeg dependencies...")
    os.system("apt-get update && apt-get install -y ffmpeg")

st.title("Chinese to Burmese SRT Subtitle Generator")
st.write("Upload a Chinese video to generate Burmese subtitles (.srt)")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mkv", "mov", "avi", "webm"])

if uploaded_file is not None:
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.info("Processing Chinese Speech & Translating to Burmese...")
    
    # Load Whisper Model
    model = whisper.load_model("base")
    
    # Chinese speech -> English transcription
    result = model.transcribe(video_path, task="translate")
    
    # Initialize Translator
    translator = GoogleTranslator(source='en', target='my')
    
    srt_content = ""
    total_segments = len(result['segments'])
    progress_bar = st.progress(0)
    
    for i, segment in enumerate(result['segments'], start=1):
        start = segment['start']
        end = segment['end']
        text = segment['text'].strip()
        
        # Translate to Burmese
        try:
            translated_text = translator.translate(text)
        except Exception:
            translated_text = text
            
        def format_time(seconds):
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds - int(seconds)) * 1000)
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"
            
        srt_content += f"{i}\n{format_time(start)} --> {format_time(end)}\n{translated_text}\n\n"
        progress_bar.progress(i / total_segments)
        
    st.success("Burmese Subtitle Generated Successfully!")
    
    # Download Button
    st.download_button(
        label="Download Burmese SRT",
        data=srt_content,
        file_name="burmese_subtitles.srt",
        mime="text/plain"
    )
    
    # Clean up
    if os.path.exists(video_path):
        os.remove(video_path)
