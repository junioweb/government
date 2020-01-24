from flask import Flask
from .bureaucracy.controllers import bureaucracy

app = Flask(__name__)

app.register_blueprint(bureaucracy, url_prefix="/forms")
