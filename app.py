from flask import Flask, render_template, request, redirect, url_for, session
from funs.text_extraction import extract_text_from_pdf
from funs.gemini_call import call_gemini_api_for_summarization, call_gemini_api_for_answer

app = Flask(__name__)
app.secret_key = 'using-this-to-append-same-query-to-display-previous-queries-in-result-page'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            pdf_text = extract_text_from_pdf(file)
            summary = call_gemini_api_for_summarization(pdf_text)
            session['summary'] = summary
            session['pdf_text'] = pdf_text
            session['queries_responses'] = []
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
