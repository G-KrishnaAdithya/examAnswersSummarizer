Follow these steps to use the app

Create a config.py app and have your Google api key there in the below format 
config.py
GOOGLE_API_KEY="YOUR-API-KEY"

Create a virtual environment and activate it 
Install requirements using pip install -r requirements.txt

run app using python app.py in project directory path

Go to the url http://127.0.0.1:5000
and enjoy preparation for your exams 

# NOTE 
If you have tesseract ocr this works fine
If you dont then you can only upload pdfs and u need to make following changes in code
In text_extraction.py comment out line 42 to end and uncomment from line 1 to 37
I personally recommend you to install tesseract and use ocr integrated code because it can process individual screenshotted images so that you can get information or clarify doubts at a particular page or context



# All the Best
