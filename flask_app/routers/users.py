from flask import Blueprint, render_template, Response, url_for, redirect, flash


from flask_login import current_user

from flask_app.utils import user_service

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
def get_all_users() -> str | Response:
    users_list = user_service.get_users_list()
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))
    return render_template("index.html", users_list=users_list)


@users.route("/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int) -> str | Response:
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))
    if user := user_service.get_user_by_id(user_id=user_id):
        return render_template("detail_page.html", user=user)
    flash(message="User not found")
    return redirect(url_for("users.get_all_users"))
