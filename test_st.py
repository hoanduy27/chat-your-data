import streamlit as st
from audio_recorder_streamlit import audio_recorder
import random 

def onsubmit():
    prompt = st.session_state.prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user"):
    #     st.markdown(prompt)

    reply = prompt 

    st.session_state.messages.append({"role": "bot", "content": reply})
    # with st.chat_message("bot"):
    #     st.markdown(reply)

def render_message_box():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    wav = audio_recorder(text="Say something dirty")
    st.chat_input("Dirty me", key="prompt", on_submit=onsubmit, )
    
    if wav:
        transcription = transcribe()
        st.text(transcription)
    
    wav_sent = st.button("Send")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])

    if wav and wav_sent:
        st.session_state.messages.append({"role": "user", "content": transcription})
        with st.chat_message("user"):
            st.markdown(transcription)
        reply = transcription
        st.session_state.messages.append({"role": "bot", "content": reply})
        with st.chat_message("bot"):
            st.markdown(reply)
        transcription = ""
        wav = b""

def transcribe():
    return random.choice(["2", "3", "1"])

render_message_box()