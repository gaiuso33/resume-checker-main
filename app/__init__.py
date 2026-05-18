from flask import Flask
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)

    from app.routes.main import main_bp
    from app.routes.export import export_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(export_bp)

    return app