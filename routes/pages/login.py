from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
import sqlite3


# 创建登录和退出功能的蓝图。Login blueprint.
login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    # 页面刚打开时没有错误，登录失败后才会设置错误信息。Set an empty error.
    error = ""

    # 只有用户提交登录表单时，才读取并检查输入。Check a submitted form.
    if request.method == "POST":
        # 登录值可以是用户名或邮箱，去掉它前后的空格，但密码中的空格会保留。Get the login values.
        login_value = request.form.get("login_value", "").strip()
        password = request.form.get("password", "")

        # 如果有字段为空，就要求用户完成所有字段。Check empty fields.
        if login_value == "" or password == "":
            error = "Please complete every field."

        # 如果登录值或密码太长，就停止查询，并使用统一的错误信息。Check the length limits.
        elif len(login_value) > 100 or len(password) > 128:
            error = "Incorrect username, email or password."

        # 输入通过基本检查后，连接数据库查找用户。Find the user.
        else:
            connection = sqlite3.connect("database/app.db")
            connection.execute("PRAGMA foreign_keys = ON")
            connection.row_factory = sqlite3.Row

            # 使用不区分大小写的查询，让用户可以使用用户名或邮箱登录。Search by username or email.
            user = connection.execute(
                """
                SELECT id, username, email, password_hash
                FROM user
                WHERE username = ? COLLATE NOCASE
                OR email = ? COLLATE NOCASE
                """,
                (login_value, login_value)
            ).fetchone()

            # 用户资料读取完成后关闭数据库连接。Close the database.
            connection.close()

            # 如果找不到用户或密码哈希检查失败，就显示相同的登录错误。Check the password.
            if user is None or not check_password_hash(
                user["password_hash"],
                password
            ):
                error = "Incorrect username, email or password."

            # 登录成功后，把用户ID和用户名存入session，并返回主页。Start the user session.
            else:
                session["user_id"] = user["id"]
                session["username"] = user["username"]

                return redirect("/")

    # 第一次打开页面或登录失败时，显示登录页面和错误信息。Show the login page.
    return render_template(
        "login.html",
        error=error
    )


@login_bp.route("/logout")
def logout():
    # 清除session中的用户资料，让当前用户退出登录。Clear the session.
    session.clear()

    # 退出完成后返回网站主页。Return to the home page.
    return redirect("/")