import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload size