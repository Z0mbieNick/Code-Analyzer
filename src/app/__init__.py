from flask import Flask
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "instance/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views
