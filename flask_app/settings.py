import os

from dotenv import load_dotenv

load_dotenv()


def get_sqalchemy_link(environment: str) -> str:
    if environment == "HOME":
        return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('PG_HOST')}:{int(os.getenv('PG_PORT'))}/{os.getenv('DB_NAME')}"
    else:
        return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DEV_PASS')}@{os.getenv('DEV_HOST')}:{int(os.getenv('PG_PORT'))}/{os.getenv('DB_NAME')}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    TEMPLATES_FOLDER = "/static/templates"
    SQLALCHEMY_DATABASE_URI = get_sqalchemy_link(environment=os.getenv("ENVIRONMENT"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True if os.getenv("DEBUG") == "True" else False
