from dotenv import load_dotenv
import requests
import base64
import os
from query_handler import handle_query

load_dotenv()
sarvamapikey = os.getenv("sarvamapikey")

def text_to_speech_from_query(query, chunks):
    # Handle the query and get the generated response text
    response = handle_query(query, chunks)
    generated_text = response['response']  # Extract the response content

    # Ensure the generated text does not exceed 500 characters
    if len(generated_text) > 500:
        print(f"Warning: Generated text exceeds 500 characters. Truncating to 500 characters.")
        generated_text = generated_text[:500]

    # Translate the generated text
    url_translate = "https://api.sarvam.ai/translate"
    payload_translate = {
        "input": generated_text,
        "source_language_code": "en-IN",
        "target_language_code": "hi-IN",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True
    }

    headers = {
        "Content-Type": "application/json",
        'API-Subscription-Key': sarvamapikey
    }

    # Make the request for translation
    translate_response = requests.post(url_translate, json=payload_translate, headers=headers)

    if translate_response.status_code != 200:
        print(f"Error in translation: {translate_response.status_code}, {translate_response.text}")
        return "Translation error", None

    translated_text = translate_response.text.strip()

    # Convert the translated text to speech
    url_speech = "https://api.sarvam.ai/text-to-speech"
    payload_speech = {
        "target_language_code": "hi-IN",
        "inputs": [translated_text],
        "speaker": "amol",
        "pitch": 0,
        "pace": 1.40,
        "Loudness": 2,
        "speech_sample_rate": 16000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }

    # Make the request for text-to-speech
    speech_response = requests.post(url_speech, json=payload_speech, headers=headers)

    if speech_response.status_code == 200:
        audio_string = speech_response.text[12:-3]
        audio_data = base64.b64decode(audio_string)

        file_path = "output_speech.wav"
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        print(f"Audio saved as {file_path}")
        return translated_text, audio_data
    else:
        print(f"Error in speech generation: {speech_response.status_code}, {speech_response.text}")
        return translated_text, None
