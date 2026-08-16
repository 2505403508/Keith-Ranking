from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
import sqlite3


login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        login_value = request.form.get("login_value", "").strip()
        password = request.form.get("password", "")

        if login_value == "" or password == "":
            error = "Please complete every field."

        elif len(login_value) > 100 or len(password) > 128:
            error = "Incorrect username, email or password."

        else:
            connection = sqlite3.connect("database/app.db")
            connection.row_factory = sqlite3.Row

            user = connection.execute(
                """
                SELECT id, username, email, password_hash
                FROM user
                WHERE username = ? COLLATE NOCASE
                OR email = ? COLLATE NOCASE
                """,
                (login_value, login_value)
            ).fetchone()

            connection.close()

            if user is None or not check_password_hash(
                user["password_hash"],
                password
            ):
                error = "Incorrect username, email or password."

            else:
                session["user_id"] = user["id"]
                session["username"] = user["username"]

                return redirect("/")

    return render_template(
        "login.html",
        error=error
    )


@login_bp.route("/logout")
def logout():
    session.clear()

    return redirect("/")