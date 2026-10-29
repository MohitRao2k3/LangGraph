from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import streamlit as st
import uuid

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state.message_history = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


# thread_id = generate_thread_id()


# **************************************** Session Setup ******************************
# st.session_state is a dictionary that stores message temporarily until page is hard refreshed 
if "message_history" not in st.session_state:
    st.session_state.message_history = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads']:
    st.sidebar.text(str(thread_id))

# **************************************** Main UI *************************************
for message in st.session_state.message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type Here')

if user_input : 
    # adding messages to list also
    st.session_state.message_history.append({"role" : "user" , "content" : user_input})
    
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {"configurable":{"thread_id": st.session_state["thread_id"]}}
    
    stream = chatbot.stream({'messages' : [HumanMessage(content=user_input)]},config=CONFIG,stream_mode="messages")
    ai_message = st.write_stream(message_chunk.text for message_chunk, metadata in stream)
    st.session_state.message_history.append({"role" : "assistant" , "content" : ai_message})