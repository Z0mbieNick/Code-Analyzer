from flask import Flask, send_from_directory, current_app
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "instance/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



from app import views    # keep this at the end so routes in views are registered
