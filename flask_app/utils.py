from typing import Any

from aiogram.types import Chat
from sqlalchemy import ScalarResult

from flask_app.models import User, db


class UserService:
    """
    Service for typical operations, such as get users, delete, create
    """

    def __init__(self):
        self.db = db

    def create_user(
        self,
        user_id: int,
        user_name: str,
        first_name: str,
        password: str,
        gender: str,
        age: int,
        phone: str,
        is_premium: bool,
        last_name: str = "Not mentioned",
        bio: str = "Empty",
        photo_url: str = "None",
    ) -> str | None:
        try:
            self.db.session.add(
                User(
                    user_id=user_id,
                    user_name=user_name,
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    photo_url=photo_url,
                    password=password,
                    gender=gender,
                    age=age,
                    phone=phone,
                    is_premium=is_premium,
                )
            )
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()

            return "Sorry, something go wrong when try to create user, try again"

    def get_user_by_id(self, user_id: int) -> Any:
        user = self.db.session.execute(
            db.select(User).where(User.user_id == user_id)
        ).scalar_one_or_none()
        return user

    def get_user_by_username(self, user_name: str) -> Any:
        user = self.db.session.execute(
            db.select(User).where(User.user_name == user_name)
        ).scalar_one_or_none()
        return user

    def get_users_list(self) -> ScalarResult:
        users_list = self.db.session.execute(db.select(User)).scalars()
        return users_list

    def update_information(self, user_info: Chat) -> None | str:
        user = self.get_user_by_id(user_id=user_info.id)
        user.bio = user_info.bio
        user.user_name = user_info.username
        user.first_name = user_info.first_name
        user.last_name = user_info.last_name
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            return "Sorry, something go wrong when try to update your info, try again"

    def delete_account(self, user_id: int) -> str | None:
        user = self.get_user_by_id(user_id=user_id)
        try:
            self.db.session.delete(user)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            return (
                "Sorry, something go wrong when try to delete your account, try again"
            )


user_service = UserService()
