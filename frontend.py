import streamlit as st
from dotenv import load_dotenv
from document_loader import load_documents
from speech import text_to_speech_from_query
import requests

load_dotenv()

file_path = "data/ncert.pdf"
chunks = load_documents(file_path)

# Function to handle querying notes
def query_ncert_notes(query):
    try:
        response = requests.post('http://127.0.0.1:8000/query/', json={'question': query})
        response.raise_for_status()
        data = response.json()
        return data.get('response', 'No response received.')
    except requests.exceptions.RequestException as e:
        return f'Error querying notes: {e}'

# Function to translate text using the API
def translate_text(text):
    try:
        response = requests.post('http://127.0.0.1:8000/translate/', json={'text': text})
        response.raise_for_status()
        data = response.json()
        return data.get('translated_text', 'No translation received.')
    except requests.exceptions.RequestException as e:
        return f'Error translating text: {e}'

# Function to generate a random question
def generate_random_question():
    try:
        response = requests.get('http://127.0.0.1:8000/generate-question/')
        response.raise_for_status()
        data = response.json()
        return data.get('question', 'No question generated.')
    except requests.exceptions.RequestException as e:
        return f'Error generating question: {e}'

# Streamlit app layout
st.set_page_config(page_title="NCERT Quiz & Text to Speech App", layout="wide")
st.title('NCERT Quiz & Text to Speech App')

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option:", ("Welcome", "Query Notes", "Text to Speech", "Practice Questions"))

# Welcome page
if option == "Welcome":
    st.header("Welcome to the NCERT App!")
    st.write("This app allows you to query NCERT notes, audio notes, and generate questions for practice.")
    st.write("Use the sidebar to navigate between options.")

# Query NCERT Notes section
elif option == "Query Notes":
    st.header('Query NCERT Notes')
    query = st.text_input("Enter your query")
    if st.button('Query'):
        with st.spinner('Querying...'):
            query_response = query_ncert_notes(query)
            st.success('Response:')
            st.write(query_response)
            
# Text to Speech section
elif option == "Audio Notes":
    st.header("Audio Sound Notes")
    st.write("Enter your query below and press 'Generate' to convert the text to speech.")
    query = st.text_input("Your Query:", "")
    if st.button("Generate"):
        if query:
            with st.spinner("Generating response..."):
                result = text_to_speech_from_query(query, chunks)
            if result:
                translated_text, audio_data = result
                if audio_data:
                    st.audio(audio_data, format='audio/wav')
                    st.success("Audio generated successfully!")
                    st.text_area("Translated Text:", translated_text, height=200)
                else:
                    st.error("Audio generation failed. Please check the console for errors.")
            else:
                st.error("An unexpected error occurred. Please try again.")
        else:
            st.warning("Please enter a query before generating.")

# Generate Random Question section
elif option == "Practice Questions":
    st.header('Generate Question')
    if st.button('Generate Question'):
        with st.spinner('Generating...'):
            generated_question = generate_random_question()
            st.success('Generated Question:')
            st.write(generated_question)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Utkash Kumar")
