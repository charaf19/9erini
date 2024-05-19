from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Bring in streamlit for UI dev
import streamlit as st

#seteup the app tittle 
st.title('Sowel 9errini')

#setup a session state message variable to hold all the old messages
if 'messages' not in st.session_state:
    #display the prompt
    st.session_state.messages = []

#display all the historical messages 
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

#build a prompt input template to display the prompts 
prompt = st.chat_input('Pass your Prompt Here')

#if the user hits enter then 
if prompt:
    #display the prompt
    st.chat_message('user').markdown(prompt)
    #store the user prompt in the state
    st.session_state.messages.append({'role':'user','content':prompt})
