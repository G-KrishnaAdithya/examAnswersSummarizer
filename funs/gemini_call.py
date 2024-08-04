from config import GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

def call_gemini_api_for_summarization(pdf_text): 
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message("Please Summarize the following text: " + pdf_text)
    return response.text if response else None

def call_gemini_api_for_answer(pdf_text, query): 
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message("From the following text: " + pdf_text + " please answer this Question: " + query)
    return response.text if response else None
