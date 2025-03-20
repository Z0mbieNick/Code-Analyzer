from flask import Flask
import os

app = Flask(__name__)

# Set upload folder BEFORE importing views
UPLOAD_FOLDER = os.path.join(os.getcwd(), "instance/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views  # Import after config is set
