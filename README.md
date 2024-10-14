# NCERT Quiz & Text-to-Speech App

### Overview
The NCERT Quiz & Text-to-Speech App is a Python-based application that allows users to interact with NCERT documents (e.g., PDFs), ask questions related to sound concepts, generate quiz questions, and convert the text responses into speech. It features a command-line interface (CLI) and a web-based interface powered by Streamlit, as well as API endpoints built with FastAPI.

### Features
- **Query NCERT Notes**: Ask questions related to the NCERT content and get concise, AI-generated responses.
- **Generate Quiz Questions**: Automatically generate quiz questions based on the document content.
- **Text-to-Speech**: Convert query responses into speech in multiple languages.
- **API Endpoints**: Provides a FastAPI interface to query, generate quiz questions, and translate text.
- **Streamlit Web Interface**: Offers a user-friendly web interface for querying and generating questions.

### Prerequisites
- Python 3.8 or higher
- Required Python libraries: 
  - `faiss`, `streamlit`, `langchain`, `pydantic`, `huggingface_hub`, `uvicorn`, `dotenv`, `requests`, `numpy`, `sklearn`
  
### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/NCERT-quiz-text-speech.git
    cd NCERT-quiz-text-speech
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your environment variables in a `.env` file:
    ```
    HUGGINGFACE_API_KEY=your_huggingface_api_key
    sarvamapikey=your_sarvam_api_key
    ```

### Usage

#### Running the Application

1. **Run the FastAPI server**:
    ```bash
    uvicorn api:app --reload
    ```
    This will start the API server at `http://127.0.0.1:8000/`.

2. **Run the Streamlit frontend**:
    ```bash
    streamlit run frontend.py
    ```

3. **Command Line Interface**:
    You can interact with the app via CLI by running `main.py`:
    ```bash
    python main.py
    ```

#### Features
- **Query Notes**: Use the `/query/` endpoint to ask questions and get relevant notes from the NCERT content.
- **Generate Quiz**: Use the `/generate-question/` endpoint to get random quiz questions.
- **Text-to-Speech**: Use the `/translate/` endpoint to translate and convert text to speech.


### Contribution
If you'd like to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request!

