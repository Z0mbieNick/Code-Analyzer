from flask import Flask, render_template, request
import os
import ast
import re

app = Flask(__name__)
UPLOAD_FOLDER = "instance/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

INSECURE_PATTERNS = {
    "eval": r"\beval\s*\(",
    "exec": r"\bexec\s*\(",
    "hardcoded_secret": r"(?i)\b(password|api_key|secret|token)\s*=\s*[\"'].*?[\"']",
    "insecure_hashing": r"\bhashlib\.(md5|sha1)\s*\(",
    "insecure_random": r"\brandom\.(randint|choice|random)\(",
    "subprocess": r"\bsubprocess\.(run|Popen|call|check_output)\(",
    "pickle_load": r"\bpickle\.load\s*\(",
    "csrf_missing": r"<form[^>]*method=['\"]POST['\"][^>]*>(?!.*csrf_token\(\))"
}

class SecurityChecker(ast.NodeVisitor):
    def __init__(self, code):
        self.issues = []
        self.code = code.split("\n")
    
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.issues.append((node.lineno, "Division by zero detected!"))
            else:
                self.issues.append((node.lineno, "Potential division by zero, consider using try-except."))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec"]:
            self.issues.append((node.lineno, f"Use of {node.func.id} is dangerous due to code injection risks."))
        self.generic_visit(node)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and file.filename.endswith('.py'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return analyze_file(filepath)
    return render_template('index.html')

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    tree = ast.parse(code)
    checker = SecurityChecker(code)
    checker.visit(tree)
    for pattern_name, pattern in INSECURE_PATTERNS.items():
        for i, line in enumerate(code.split("\n"), start=1):
            if re.search(pattern, line):
                checker.issues.append((i, f"Potential security issue: {pattern_name} found."))
    return render_template('results.html', issues=checker.issues)

if __name__ == '__main__':
    app.run(debug=True)