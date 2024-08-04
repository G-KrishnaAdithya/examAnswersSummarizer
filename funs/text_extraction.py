# import fitz  # PyMuPDF
# import re

# def preprocess_text(text):
#     # Remove unnecessary spaces and newlines
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def extract_text_from_file(file_stream):
#     try:
#         # Ensure the file is a PDF
#         if not file_stream.filename.endswith('.pdf'):
#             raise ValueError("Unsupported file type. Please provide a 'pdf'.")

#         # Convert the PDF file stream to a byte array
#         file_bytes = file_stream.read()

#         # Use PyMuPDF to open the PDF
#         doc = fitz.open(stream=file_bytes, filetype="pdf")

#         text = ""
#         for page in doc:
#             # Extract text directly from the PDF
#             page_text = page.get_text()
#             text += page_text + "\n"

#         # Preprocess the text
#         processed_text = preprocess_text(text)

#         # Check if the text length exceeds 4000 characters
#         if len(processed_text) > 4000:
#             return processed_text[:4000], True

#         return processed_text, False
    
#     except Exception as e:
#         return f"An error occurred during text extraction: {e}", False

#the above is without ocr
#the below is with ocr

import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import re

def preprocess_text(text):
    # Remove unnecessary spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_text_from_file(file_stream):
    try:
        file_type = 'pdf' if file_stream.filename.endswith('.pdf') else 'image'
        text = ""
        
        if file_type.lower() == 'pdf':
            # Convert the PDF file stream to a byte array
            file_bytes = file_stream.read()

            # Use PyMuPDF to open the PDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")

            for page in doc:
                # Try to extract text directly from the PDF
                page_text = page.get_text()
                if not page_text.strip():
                    # If direct text extraction fails, use OCR
                    images = convert_from_bytes(file_bytes, first_page=page.number+1, last_page=page.number+1)
                    for image in images:
                        page_text += pytesseract.image_to_string(image)
                
                text += page_text + "\n"

        elif file_type.lower() == 'image':
            # Open the image file stream
            image = Image.open(file_stream)

            # Perform OCR on the image and extract text
            text = pytesseract.image_to_string(image)

        else:
            raise ValueError("Unsupported file type. Please provide 'pdf' or 'image'.")
        
        # Preprocess the text
        processed_text = preprocess_text(text)
        
        # Check if the text length exceeds 4000 characters
        if len(processed_text) > 4000:
            return processed_text[:4000], True
        
        return processed_text, False
    
    except Exception as e:
        return f"An error occurred during text extraction: {e}", False

