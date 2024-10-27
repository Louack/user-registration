import os

from dotenv import load_dotenv

load_dotenv()

# REPOSITORIES
USER_REPO = os.environ.get("USER_REPO", "mysql_user_repo")
ACTIVATION_CODE_REPO = os.environ.get(
    "ACTIVATION_CODE_REPO", "mysql_activation_code_repo"
)

# SERVICES
PASSWORD_ENCODER = os.environ.get("PASSWORD_ENCODER", "dummy_password_encoder")
EMAIL_SERVICE = os.environ.get("EMAIL_SERVICE", "dummy_email_service")

# MYSQL
MYSQL_DB_HOST = os.environ.get("MYSQL_DB_HOST", "db")
MYSQL_DB_NAME = os.environ.get("MYSQL_DB_NAME", "db")
MYSQL_DB_USER = os.environ.get("MYSQL_DB_USER", "root")
MYSQL_DB_PASSWORD = os.environ.get("MYSQL_DB_PASSWORD", "root_password")
