import streamlit as st
import requests
from PIL import Image
import pytesseract
from transformers import pipeline

access_token = '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'

# Initialize the image captioning pipeline
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base", token=access_token)

# Function to query the Hugging Face API
def query_huggingface_api(prompt):
    API_URL = "https://jrliticly0nlznb9.us-east-1.aws.endpoints.huggingface.cloud"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token} ",
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
        st.markdown(f"**{message['role']}**: {message['content']}")

# Function to handle user input
def handle_user_input(prompt, uploaded_file):
    if prompt:
        # Display the prompt
        st.session_state.messages.append({'role': 'User', 'content': prompt})
        # Query the Hugging Face API
        response = query_huggingface_api(prompt)
        if response:
            # Show the assistant response
            st.session_state.messages.append({'role': 'Assistant', 'content': response})
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Get the image caption
        caption = get_image_caption(image)
        st.session_state.messages.append({'role': 'User', 'content': f"**Image Caption:** {caption}"})

        # Extract text from the image
        extracted_text = extract_text_from_image(image)

        # Simplify the extracted text using the Hugging Face API
        simplified_text = simplify_text_with_hf_api(extracted_text)

        # Display the simplified text
        st.session_state.messages.append({'role': 'Assistant', 'content': f"**Simplified Text:** {simplified_text}"})


# Function to get image caption
def get_image_caption(image):
    return captioner(image)[0]['generated_text']

# Function to get the text from the image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to simplify text using the Hugging Face API
def simplify_text_with_hf_api(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
      "Accept" : "application/json",
      "Authorization": "Bearer hf_XXXXX",
      "Content-Type": "application/json"
    }
    prompt = f"Explain this to a child and make it easy to understand: {text}"
    data = {
        "inputs": prompt,
        "parameters": {
            "max_length": 512,
            "num_beams": 4,
            "early_stopping": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        simplified_text = response.json()[0]['generated_text']
        return simplified_text
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Setup the app title
st.title('9errini')

# Initialize session state for messages if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all historical messages
display_chat_messages()

# Create an input container with text input and send button
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    prompt = st.text_input('Your message:', key='text_input')
    st.write(" ")  # Spacer
    send_button = st.button('Send', help='Click to send your message')

# File uploader button
uploaded_file = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])

# Handle user input if the send button is clicked or an image is uploaded
if send_button:
    handle_user_input(prompt, uploaded_file)
elif uploaded_file:
    handle_user_input(None, uploaded_file)
