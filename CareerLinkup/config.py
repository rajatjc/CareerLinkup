import os
import secrets


class Config:
    """Settings read from the environment, with defaults that work for local development."""

    # Without SECRET_KEY set, sessions and reset links only last until the process restarts.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///mydata.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads (resumes, photos, logos) larger than this are rejected with a 413.
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Password-reset and shortlist emails.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("CareerLinkup", os.environ.get("MAIL_SENDER", "no-reply@careerlinkup.local"))

    # Password-reset links stop working after this many seconds.
    RESET_TOKEN_MAX_AGE = 30 * 60
