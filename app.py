from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st
import requests

API_URL = "https://jrliticly0nlznb9.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}
# Function to query the Hugging Face API
def query_huggingface_api(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        st.write(response.json())  # Print the entire JSON response for debugging
        return response.json()  # Returning the entire response for now
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Setup the app title
st.title('Sowel 9errini')

# Setup a session state message variable to hold all the old messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all the historical messages
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# Build a prompt input template to display the prompts
prompt = st.chat_input('Pass your Prompt Here')

# If the user hits enter
if prompt:
    # Display the prompt
    st.chat_message('user').markdown(prompt)
    # Store the user prompt in the state
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Query the Hugging Face API
    response = query_huggingface_api(prompt)
    # Ensure response is not None
    if response:
        # Displaying response based on actual keys in the response JSON
        if 'generated_text' in response:
            assistant_response = response['generated_text']
        else:
            assistant_response = response  # Update this based on actual response format

        # Show the LLM response
        st.chat_message('assistant').markdown(assistant_response)
        # Store the LLM response in state
        st.session_state.messages.append({'role': 'assistant', 'content': assistant_response})