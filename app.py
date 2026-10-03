import streamlit as st
import requests

# Set up the look of the web page
st.set_page_config(page_title="AI Document Intelligence", layout="centered")
st.title("📂 Premium AI Document Search Engine")
st.write("Upload a corporate PDF and instantly ask questions about it.")

BACKEND_URL = "http://127.0.0.1:8000"

# Part 1: File Upload Section
uploaded_file = st.file_uploader("Choose a PDF document", type=["pdf"])

if uploaded_file is not None:
    if st.button("🚀 Process & Index Document"):
        with st.spinner("Analyzing document chunks..."):
            # Send file to our FastAPI backend
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{BACKEND_URL}/upload/", files=files)
                if response.status_code == 200:
                    st.success(f"Successfully indexed: {uploaded_file.name}")
                else:
                    st.error("Failed to process document. Make sure your backend server is running.")
            except Exception:
                st.error("Connection error. Is your backend ('py main.py') active?")

st.divider()

# Part 2: Chat Interface Section
st.subheader("💬 Chat with your Data")

# Initialize conversation memory storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user questions
if user_question := st.chat_input("What would you like to know from the documents?"):
    # Display human question immediately
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)
        
    # Send question to backend and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching document database..."):
            try:
                # FIXED: Headers and clean JSON structure to ensure connection never snaps
                headers = {"Content-Type": "application/json"}
                payload = {"question": str(user_question)}
                
                res = requests.post(f"{BACKEND_URL}/chat/", json=payload, headers=headers)
                
                if res.status_code == 200:
                    answer = res.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend returned error code: {res.status_code}. Make sure your API keys match.")
            except Exception as e:
                st.error("Connection lost. Please make sure your backend terminal ('py main.py') hasn't crashed.")
