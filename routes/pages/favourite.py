from flask import Blueprint, render_template, redirect, session, abort
import sqlite3


# 创建游戏收藏、公司收藏和收藏页面使用的蓝图。Favourite blueprint.
favourite_bp = Blueprint("favourite", __name__)


# 建立数据库连接，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
def get_connection():
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection


@favourite_bp.route("/favourites")
def favourites():
    # 未登录用户没有自己的收藏资料，所以会先被送到登录页面。Require login.
    if session.get("user_id") is None:
        return redirect("/login")

    # 打开数据库，准备读取当前用户自己的游戏和公司收藏。Open the database.
    connection = get_connection()

    # 读取当前用户收藏的所有游戏，不会显示其他用户的游戏收藏。Get favourite games.
    games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN favourite
        ON game.id = favourite.game_id

        WHERE favourite.user_id = ?
        ORDER BY game.id
        """,
        (session["user_id"],)
    ).fetchall()

    #读取当前用户收藏的公司，并计算每个公司开发和发行的游戏数量。Get favourite companies.
    companies = connection.execute(
        """
        SELECT
            company.id,
            company.name,
            company.started,

            (
                SELECT COUNT(*)
                FROM game_developer
                WHERE game_developer.company_id = company.id
            ) AS developed_count,

            (
                SELECT COUNT(*)
                FROM game_publisher
                WHERE game_publisher.company_id = company.id
            ) AS published_count

        FROM company
        JOIN company_favourite
        ON company.id = company_favourite.company_id

        WHERE company_favourite.user_id = ?
        ORDER BY company.name
        """,
        (session["user_id"],)
    ).fetchall()

    #收藏资料读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把当前用户的游戏收藏和公司收藏传给收藏页面。Show the favourites.
    return render_template(
        "favourites.html",
        games=games,
        companies=companies
    )


@favourite_bp.route(
    "/favourite/game/<int:game_id>",
    methods=["POST"]
)
def favourite_game(game_id):
    # 未登录用户不能增加或删除游戏收藏。Require login.
    if session.get("user_id") is None:
        return redirect("/login")

    # 打开数据库，准备检查游戏和修改收藏记录。Open the database.
    connection = get_connection()

    # 先确认网页地址中的游戏ID是真实存在的。Find the game.
    game = connection.execute(
        """
        SELECT id
        FROM game
        WHERE id = ?
        """,
        (game_id,)
    ).fetchone()

    # 如果游戏不存在，就关闭数据库并显示404页面。Show 404 if not found.
    if game is None:
        connection.close()
        abort(404)

    #检查这个游戏是否已经在当前用户自己的收藏中。Check the saved game.
    saved_game = connection.execute(
        """
        SELECT id
        FROM favourite
        WHERE user_id = ? AND game_id = ?
        """,
        (session["user_id"], game_id)
    ).fetchone()

    # 如果没有收藏过，就加入一条属于当前用户的游戏收藏记录。Add the favourite.
    if saved_game is None:
        connection.execute(
            """
            INSERT INTO favourite (user_id, game_id)
            VALUES (?, ?)
            """,
            (session["user_id"], game_id)
        )

    # 如果已经收藏过，就只删除当前用户的这一条收藏记录。Remove the favourite.
    else:
        connection.execute(
            """
            DELETE FROM favourite
            WHERE user_id = ? AND game_id = ?
            """,
            (session["user_id"], game_id)
        )

    # 保存收藏修改并关闭数据库连接。Save the change.
    connection.commit()
    connection.close()

    # 修改完成后返回原来的游戏详情页面。Return to the game page.
    return redirect("/game/" + str(game_id))


@favourite_bp.route(
    "/favourite/company/<int:company_id>",
    methods=["POST"]
)
def favourite_company(company_id):
    # 未登录用户不能增加或删除公司收藏。Require login.
    if session.get("user_id") is None:
        return redirect("/login")

    # 打开数据库，准备检查公司和修改收藏记录。Open the database.
    connection = get_connection()

    # 先确认网页地址中的公司ID是真实存在的。Find the company.
    company = connection.execute(
        """
        SELECT id
        FROM company
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    #如果公司不存在就关闭数据库并显示404页面。Show 404 if not found.
    if company is None:
        connection.close()
        abort(404)

    # 检查这个公司是否已经在当前用户自己的收藏中。Check the saved company.
    saved_company = connection.execute(
        """
        SELECT id
        FROM company_favourite
        WHERE user_id = ? AND company_id = ?
        """,
        (session["user_id"], company_id)
    ).fetchone()

    # 如果没有收藏过，就加入一条属于当前用户的公司收藏记录。Add the favourite.
    if saved_company is None:
        connection.execute(
            """
            INSERT INTO company_favourite (user_id, company_id)
            VALUES (?, ?)
            """,
            (session["user_id"], company_id)
        )

    # 如果已经收藏过，就只删除当前用户的这一条收藏记录。Remove the favourite.
    else:
        connection.execute(
            """
            DELETE FROM company_favourite
            WHERE user_id = ? AND company_id = ?
            """,
            (session["user_id"], company_id)
        )

    # 保存收藏修改并关闭数据库连接。Save the change.
    connection.commit()
    connection.close()

    # 修改完成后返回原来的公司详情页面。Return to the company page.
    return redirect("/company/" + str(company_id))