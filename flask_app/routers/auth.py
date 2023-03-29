from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    Response,
    url_for,
    flash,
)
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash


from flask_app.utils import user_service

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "POST":
        username_or_phone = request.form.get("username")
        password = request.form.get("password")

        if user := user_service.get_user_by_username_or_phone(
            username_or_phone=username_or_phone
        ):
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("users.get_all_users"))
            else:
                flash(message="Wrong password")
        else:
            flash(message="User not found.")
    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
def logout() -> Response:
    logout_user()
    return redirect(url_for("auth.login"))
