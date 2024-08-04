from flask import Flask, render_template, request, redirect, url_for, session, flash
from funs.text_extraction import extract_text_from_file
from funs.gemini_call import call_gemini_api_for_summarization, call_gemini_api_for_answer

app = Flask(__name__)
app.secret_key = 'using-this-to-append-same-query-to-display-previous-queries-in-result-page'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part in the request.")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No file selected for uploading.")
            return redirect(request.url)
        
        if file:
            pdf_text, is_too_large = extract_text_from_file(file)
            if pdf_text.startswith("An error occurred"):
                flash(pdf_text)
                return redirect(request.url)
            else:
                summary = call_gemini_api_for_summarization(pdf_text)
                session['summary'] = summary
                session['pdf_text'] = pdf_text
                session['queries_responses'] = []
                if is_too_large:
                    flash("The PDF is too large. Results may only cover the first few pages.\nTo get exact explanation of a page please upload the pages u want explanation for")
                return redirect(url_for('result'))
    
    return render_template('home.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    summary = session.get('summary')
    pdf_text = session.get('pdf_text')
    queries_responses = session.get('queries_responses', [])
    
    if request.method == 'POST':
        query = request.form.get('query', '')
        if pdf_text and query:
            answer = call_gemini_api_for_answer(pdf_text, query)
            queries_responses.append({'query': query, 'answer': answer})
            session['queries_responses'] = queries_responses
    
    return render_template('result.html', summary=summary, queries_responses=queries_responses)

if __name__ == '__main__':
    app.run(debug=True)
