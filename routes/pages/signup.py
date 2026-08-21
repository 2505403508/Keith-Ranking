from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
import sqlite3
import re


# 创建用户注册功能的蓝图。Sign-up blueprint.
signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    # 页面刚打开时没有错误，验证失败后才会把错误文字放进这个变量。Set an empty error.
    error = ""

    # 只有用户提交注册表单时，才读取输入并进行验证。Check a submitted form.
    if request.method == "POST":
        # 去掉用户名和邮箱前后的空格，并把邮箱转成小写，密码中的空格会原样保留。Get the form values.
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # 用户名只能使用字母、数字和下划线，邮箱需要有@、域名和点号。Set the validation patterns.
        username_pattern = r"^[A-Za-z0-9_]+$"
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        # 按顺序检查空字段、长度、格式和两次密码是否相同，发现问题后显示对应错误。Validate the form.
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

        # 所有输入通过验证后，才连接数据库并检查重复账号。Continue after validation.
        else:
            connection = sqlite3.connect("database/app.db")
            connection.execute("PRAGMA foreign_keys = ON")

            # 使用不区分大小写的查询，检查用户名或邮箱是否已经被注册。Check for an existing user.
            existing_user = connection.execute(
                """
                SELECT id
                FROM user
                WHERE username = ? COLLATE NOCASE
                OR email = ? COLLATE NOCASE
                """,
                (username, email)
            ).fetchone()

            # 如果找到相同的用户名或邮箱，就不建立新账号。Stop duplicate accounts.
            if existing_user is not None:
                error = "The username or email is already being used."

            # 如果账号没有重复，就先加密密码，再把新用户存入数据库。Create the new user.
            else:
                password_hash = generate_password_hash(password)

                connection.execute(
                    """
                    INSERT INTO user (username, email, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (username, email, password_hash)
                )

                #保存新账号并关闭数据库，然后把用户送到登录页面。Save the account.
                connection.commit()
                connection.close()

                return redirect("/login")

            # 如果注册没有成功在重新显示页面前关闭数据库连接。Close the database.
            connection.close()

    # 第一次打开页面或验证失败时，显示注册页面和错误信息。Show the sign-up page.
    return render_template(
        "signup.html",
        error=error
    )