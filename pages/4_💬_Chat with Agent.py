import streamlit as st
import json  # For saving and loading chat history
from falcon import client

# App Configuration
st.set_page_config(
    page_title="GenEstate",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

# Sidebar title
st.sidebar.title("Chat Management")

# Initialize session state variables
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False

if "username" not in st.session_state:
    st.session_state["username"] = "Undefined"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 🧠 Data Navigator at your service! Let me know what you're looking for—whether it's exploring trends, generating insights, or creating charts—and we'll dive right in! 🚀 What's your first question?",
        }
    ]

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = (
        {}
    )  # Dictionary to store saved chats: {chat_name: chat_history}

# Check authentication
isAuth = st.session_state["authentication_status"]

if isAuth:
    # Display the main title
    st.title("Agent Rick")

    # Sidebar options
    with st.sidebar:
        # Save current chat option
        chat_name = st.text_input("Save Current Chat As:", placeholder="Enter a name")
        if st.button("Save Chat"):
            if chat_name.strip():
                st.session_state.saved_chats[chat_name] = (
                    st.session_state.messages.copy()
                )
                st.success(f"Chat saved as '{chat_name}'!")
            else:
                st.error("Chat name cannot be empty!")

        # Load saved chats dropdown
        if st.session_state.saved_chats:
            selected_chat = st.selectbox(
                "Load Saved Chat:",
                options=["Select a chat"] + list(st.session_state.saved_chats.keys()),
                index=0,
            )
            if selected_chat != "Select a chat":
                # Load the selected chat
                st.session_state.messages = st.session_state.saved_chats[
                    selected_chat
                ].copy()
                st.success(f"Loaded chat: '{selected_chat}'")

        # Clear all saved chats
        if st.button("Clear Saved Chats"):
            st.session_state.saved_chats = {}
            st.success("All saved chats have been cleared!")

        # Clear current chat history
        if st.button("Clear Current Chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! 🧠 Data Navigator at your service! Let me know what you're looking for—whether it's exploring trends, generating insights, or creating charts—and we'll dive right in! 🚀 What's your first question?",
                }
            ]
            st.success("Chat history cleared!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input for chat
    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call the Falcon API to get the assistant's response
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="tiiuae/falcon-180B-chat",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            # Collect and display the streamed response
            response = st.write_stream(stream)

        # Append the response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.error("Please login first!")
