import streamlit as st
import requests
from PIL import Image
from transformers import pipeline

access_token='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'
# Initialize the image captioning pipeline
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base",token=access_token)

# Function to query the Hugging Face API
def query_huggingface_api(prompt):
    API_URL = "https://jrliticly0nlznb9.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept": "application/json",
        "Authorization":f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get('generated_text', 'No text generated.')
        else:
            return 'No valid response received.'
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Function to display chat messages
def display_chat_messages():
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

# Function to handle user input
def handle_user_input(prompt, uploaded_file):
    if prompt:
        # Display the prompt
        st.chat_message('user').markdown(prompt)
        # Store the user prompt in the session state
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        # Query the Hugging Face API
        response = query_huggingface_api(prompt)
        if response:
            assistant_response = response
            # Show the LLM response
            st.chat_message('assistant').markdown(assistant_response)
            # Store the LLM response in session state
            st.session_state.messages.append({'role': 'assistant', 'content': assistant_response})
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        # Get the image caption
        caption = get_image_caption(image)
        # Display the image caption
        st.chat_message('user').markdown(f"**Image Caption:** {caption}")
        st.session_state.messages.append({'role': 'user', 'content': f"**Image Caption:** {caption}"})

# Function to get image caption
def get_image_caption(image):
    return captioner(image)[0]['generated_text']

# Setup the app title
st.title('Sowel 9errini')

# Initialize session state for messages if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all historical messages
display_chat_messages()

# Custom CSS to style the file uploader button
st.markdown("""
    <style>
    .input-container {
        display: flex;
        align-items: center;
    }
    .text-input {
        flex-grow: 1;
        margin-right: 5px;
    }
    .upload-button {
        margin-left: 5px;
        padding: 5px;
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        background-color: #f0f0f0;
        cursor: pointer;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# Create an input container with text input, send button, and file uploader
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Text input for the prompt
prompt = st.text_input('', placeholder='Pass your Prompt Here', key='text_input', help='Type your message here and hit enter or click Send')

# Send button
send_button = st.button('Send', key='send_button', help='Click to send your message')

# File uploader button
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# Handle user input if the send button is clicked or an image is uploaded
if send_button:
    handle_user_input(prompt, uploaded_file)
elif uploaded_file:
    handle_user_input(None, uploaded_file)
