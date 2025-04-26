from flask import render_template, request
import os
import ast
from app import app   # ← THIS imports the real app
from app.models import SecurityChecker

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part uploaded.", 400  # Always return
        file = request.files['file']
        if file.filename == '':
            return "No file selected.", 400
        if file and (file.filename.endswith('.py') or file.filename.endswith('.html')):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return analyze_file(filepath)
        else:
            return "Invalid file type. Only .py or .html files allowed.", 400
    return render_template('index.html')


def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    tree = ast.parse(code)
    checker = SecurityChecker(code)
    checker.visit(tree)          # <-- you forgot (tree) here!
    checker.run_regex_checks()   # <-- regex patterns run
    return render_template('results.html', issues=checker.issues)  # <-- and return the result page!
