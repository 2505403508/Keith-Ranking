from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
import sqlite3
import re


signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        username_pattern = r"^[A-Za-z0-9_]+$"
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if (
            username == ""
            or email == ""
            or password == ""
            or confirm_password == ""
        ):
            error = "Please complete every field."

        elif len(username) < 3:
            error = "Username must be at least 3 characters."

        elif len(username) > 20:
            error = "Username must be 20 characters or fewer."

        elif re.fullmatch(username_pattern, username) is None:
            error = "Username can only use letters, numbers and underscores."

        elif len(email) > 100:
            error = "Email must be 100 characters or fewer."

        elif re.fullmatch(email_pattern, email) is None:
            error = "Please enter a valid email address."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        elif len(password) > 128:
            error = "Password must be 128 characters or fewer."

        elif password != confirm_password:
            error = "The passwords do not match."

        else:
            connection = sqlite3.connect("database/app.db")

            existing_user = connection.execute(
                """
                SELECT id
                FROM user
                WHERE username = ? COLLATE NOCASE
                OR email = ? COLLATE NOCASE
                """,
                (username, email)
            ).fetchone()

            if existing_user is not None:
                error = "The username or email is already being used."

            else:
                password_hash = generate_password_hash(password)

                connection.execute(
                    """
                    INSERT INTO user (username, email, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (username, email, password_hash)
                )

                connection.commit()
                connection.close()

                return redirect("/login")

            connection.close()

    return render_template(
        "signup.html",
        error=error
    )