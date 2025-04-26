import ast
import re

INSECURE_PATTERNS = {
    "eval usage": r"\beval\s*\(",
    "exec usage": r"\bexec\s*\(",
    "hardcoded secret": r"(?i)\b(password|api_key|secret|token)\s*=\s*[\"'].*?[\"']",
    "insecure hashing": r"\bhashlib\.(md5|sha1)\s*\(",
    "insecure random": r"\brandom\.(randint|choice|random)\(",
    "subprocess usage": r"\bsubprocess\.(run|Popen|call|check_output)\(",
    "pickle load": r"\bpickle\.load\s*\(",
    "csrf missing": r"<form[^>]*method=['\"]POST['\"][^>]*>(?!.*csrf_token\(\))"
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
                self.issues.append((node.lineno, "Potential division by zero (consider try-except)."))
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ['pickle', 'subprocess', 'hashlib', 'random']:
                self.issues.append((node.lineno, f"Suspicious import detected: {alias.name}"))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
            self.issues.append((node.lineno, f"Dangerous function used: {node.func.id}"))
        self.generic_visit(node)

    def run_regex_checks(self):
        for pattern_name, pattern in INSECURE_PATTERNS.items():
            for i, line in enumerate(self.code, start=1):
                if re.search(pattern, line):
                    self.issues.append((i, f"Pattern detected: {pattern_name}"))
