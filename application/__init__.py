from flask import Flask
from .config import configure_app
from .bureaucracy.controllers import bureaucracy

app = Flask(
    __name__,
    instance_relative_config=False
)

configure_app(app)

app.register_blueprint(bureaucracy, url_prefix="/forms")
