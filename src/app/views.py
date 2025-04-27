from flask import Flask, render_template, request, redirect, url_for, session
import os
import ast
from app import app
from app.models import SecurityChecker

# Enable sessions
app.secret_key = 'your_secret_key'  # Needed for flashing info across requests

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part uploaded.", 400
        file = request.files['file']
        if file.filename == '':
            return "No file selected.", 400
        if file and file.filename.endswith('.py'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return analyze_file(filepath)
        else:
            return "Invalid file type. Only .py files allowed.", 400

    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part uploaded.", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected.", 400
    if file and file.filename.endswith('.py'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        session['success_message'] = "✅ File successfully uploaded!"
        session['uploaded_file'] = file.filename
        return redirect(url_for('index'))
    else:
        return "Invalid file type. Only .py files allowed.", 400

@app.route('/analyze', methods=['POST'])
def analyze():
    filename = session.get('uploaded_file')
    if not filename:
        return "No file uploaded yet.", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return analyze_file(filepath)

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = ast.parse(code)
    checker = SecurityChecker(code)
    checker.visit(tree)
    checker.run_regex_checks()

    return render_template('results.html', issues=checker.issues)
