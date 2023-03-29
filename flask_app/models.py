from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask_app.database import Base

db = SQLAlchemy(metadata=Base.metadata)


class User(Base):
    """
    Model for User instance, where saved all collected automatically and manually info
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String(32), unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64), nullable=True, default="Not mentioned")
    photo_url = Column(String(100), nullable=True, default="None")
    bio = Column(String(140), nullable=True, default="User does not have bio")
    password = Column(String(256), nullable=False)
    phone = Column(String(13), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(6), nullable=False)
    is_premium = Column(Boolean, nullable=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None
