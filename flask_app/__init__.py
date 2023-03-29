from typing import Any

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from flask_app.models import db, User
from flask_app.routers import auth, users
from flask_app.settings import Config
from flask_app.database import db_session, Base

load_dotenv()

migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(users.users)
    app.register_blueprint(auth.auth)
    app.config.from_object(Config)
    db.init_app(app)
    from flask_app import models

    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id) -> Any | None:
        try:
            return db.session.execute(
                select(User).where(User.user_id == user_id)
            ).scalar_one()
        except NoResultFound:
            return False

    return app


app = create_app()
