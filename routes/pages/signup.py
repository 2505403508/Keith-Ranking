from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
import sqlite3


signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if username == "" or email == "" or password == "":
            error = "Please complete every field."

        elif len(username) < 3:
            error = "Username must be at least 3 characters."

        elif "@" not in email:
            error = "Please enter a valid email address."

        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        elif password != confirm_password:
            error = "The passwords do not match."

        else:
            connection = sqlite3.connect("database/app.db")

            existing_user = connection.execute(
                """
                SELECT id
                FROM user
                WHERE username = ? OR email = ?
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