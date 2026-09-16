import streamlit as st
import whisper
import srt
import tempfile
from datetime import timedelta

st.set_page_config(page_title="AI Subtitle Tool", page_icon="🎬")
st.title("🎬 တရုတ်-မြန်မာ Auto Subtitle Generator")
st.write("တရုတ်ဇာတ်လမ်းတွဲ ဗီဒီယို တင်ပေးပါ၊ SRT စာတန်းထိုး ထုတ်ပေးပါမည်။")

uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင် ရွေးပါ", type=["mp4", "mkv", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("🚀 SRT စာတန်းထိုး စတင်ထုတ်ယူမည်"):
        with st.spinner("AI က စာတန်းထိုး ပြုလုပ်နေပါသည်... ခဏစောင့်ပါ"):
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            model = whisper.load_model("tiny")
            result = model.transcribe(tfile.name, language="zh")
            
            subtitles = []
            for index, segment in enumerate(result['segments'], start=1):
                sub_item = srt.Subtitle(
                    index=index,
                    start=timedelta(seconds=segment['start']),
                    end=timedelta(seconds=segment['end']),
                    content=segment['text']
                )
                subtitles.append(sub_item)
            
            srt_output = srt.compose(subtitles)
            
            st.success("✅ စာတန်းထိုး ထုတ်ယူပြီးပါပြီ။")
            st.download_button(
                label="📥 SRT File Download ဆွဲမည်",
                data=srt_output,
                file_name="chinese_subtitle.srt",
                mime="text/plain"
            )
