import fitz  # install PyMuPDF to import fitz
def extract_text_from_pdf(file_stream):
    # You'll need to adapt this function to read from a file stream if it currently expects a file path.
    # Example adaptation using PyMuPDF (Fitz):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text