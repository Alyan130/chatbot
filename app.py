from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv(".env.local")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
st.title(":blue[Chat Nova] 🤖")
st.write("A futuristic AI companion!, Developed by:red[ ALYAN ALI] ")

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
 with st.spinner("Loading..."):
   for messages in st.session_state.messages:
     with st.chat_message(messages["role"]):
        st.markdown(messages["content"])

prompt = st.chat_input("Ask anything")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

       
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,  
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response) 

       
        st.session_state.messages.append({"role": "assistant", "content": full_response})


