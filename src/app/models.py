import ast
import re

class SecurityChecker(ast.NodeVisitor):
    INSECURE_PATTERNS = {
        "eval usage": (r"\beval\s*\(", "Critical"),
        "exec usage": (r"\bexec\s*\(", "Critical"),
        "hardcoded secret": (r"(?i)\b(password|api_key|secret|token)\s*=\s*[\"'].*?[\"']", "Warning"),
        "insecure hashing": (r"\bhashlib\.(md5|sha1)\s*\(", "Warning"),
        "insecure random": (r"\brandom\.(randint|choice|random)\(", "Info"),
        "subprocess usage": (r"\bsubprocess\.(run|Popen|call|check_output)\(", "Critical"),
        "pickle load": (r"\bpickle\.load\s*\(", "Critical")
    }

    def __init__(self, code):
        self.issues = []
        self.code = code.split("\n")

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.issues.append((node.lineno, "Critical", "Division durch Null erkannt!"))
            else:
                self.issues.append((node.lineno, "Warning", "Mögliche Division durch Null (bitte try-except erwägen)."))
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ['pickle', 'subprocess', 'hashlib', 'random']:
                severity = "Info" if alias.name == "random" else "Warning"
                self.issues.append((node.lineno, severity, f"Verdächtiger Import entdeckt: {alias.name}"))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
            self.issues.append((node.lineno, "Critical", f"Gefährliche Funktion verwendet: {node.func.id}"))
        self.generic_visit(node)

    def run_regex_checks(self):
        for pattern_name, (pattern, severity) in self.INSECURE_PATTERNS.items():
            for i, line in enumerate(self.code, start=1):
                if re.search(pattern, line):
                    self.issues.append((i, severity, f"Muster erkannt: {pattern_name}"))
