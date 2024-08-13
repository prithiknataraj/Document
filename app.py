from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

def translate(text, target='ta'):
    output = translator.translate(text, target).text
    return output

def chunk_and_translate(text, lang, chunk=200):
    translated_text = ''
    for i in range(0, len(text), chunk):
        chunked = text[i:i+chunk]
        translatedchunk = translate(chunked, lang)
        a= translatedchunk.replace("\n", " ")
        translated_text+= " "+ a
    
    return translated_text

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = ""
    translated_text = []
    highlighted_text = ""
    lang = ""  # Set a default value for lang

    if request.method == 'POST':
        lang = request.form['lang']
        pdf_file = request.files['pdf_file']

        if pdf_file and lang:
            # Read PDF content
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                original_text += page.extract_text()
                a= original_text.replace("\n", " ")
                original_text= a

            # Translate PDF content
            translated_text = chunk_and_translate(original_text, lang)

    if original_text and translated_text:
        # Combine original and translated sentences for highlighting
        highlighted_text = '\n'.join(f'<span class="highlight" title="{trans}">{orig}</span>'
                                     for orig, trans in zip(original_text.split('\n'), translated_text))

    return render_template('index.html', original_text=original_text, highlighted_text=highlighted_text, lang=lang, translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
