from flask import Blueprint, render_template, request, abort, session
import sqlite3


# 创建公司列表和公司详情页面使用的蓝图。Company pages blueprint.
pd_bp = Blueprint("pd", __name__)


@pd_bp.route("/pd")
def all_companies():
    # 获取公司搜索框内容，去掉前后空格，再限制为最多100个字符。Clean the search text.
    search = request.args.get("search", "").strip()
    search = search[:100]

    # 连接数据库，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 如果搜索框为空，就读取全部公司，并计算每个公司开发和发行的游戏数量。Get all companies.
    if search == "":
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
            ORDER BY company.name
            """
        ).fetchall()

    # 如果用户输入了文字，就查找名称中包含这些文字的公司。Search by company name.
    else:
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
            WHERE company.name LIKE ?
            ORDER BY company.name
            """,
            ("%" + search + "%",)
        ).fetchall()

    # 公司数据读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把公司列表和处理后的搜索文字传给公司页面。Show the company list.
    return render_template(
        "pd.html",
        companies=companies,
        search=search
    )


@pd_bp.route("/company/<int:company_id>")
def company_detail(company_id):
    # 打开数据库并设置查询格式，准备读取公司详情。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 使用网页地址中的公司ID查找对应的公司。Find the selected company.
    company = connection.execute(
        """
        SELECT id, name, started
        FROM company
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    # 如果数据库里没有这个公司ID，就关闭连接并显示404页面。Show 404 if not found.
    if company is None:
        connection.close()
        abort(404)

    # 从开发关联表中读取这个公司开发过的所有游戏。Get developed games.
    developed_games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN game_developer
        ON game.id = game_developer.game_id

        WHERE game_developer.company_id = ?
        ORDER BY game.id
        """,
        (company_id,)
    ).fetchall()

    # 从发行关联表中读取这个公司发行过的所有游戏。Get published games.
    published_games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN game_publisher
        ON game.id = game_publisher.game_id

        WHERE game_publisher.company_id = ?
        ORDER BY game.id
        """,
        (company_id,)
    ).fetchall()

    # 默认设置为没有收藏，因为未登录用户没有自己的收藏记录。Set the default status.
    is_favourite = False

    # 用户登录后，检查这个公司是否在当前用户自己的收藏中。Check this user's favourites.
    if session.get("user_id") is not None:
        saved_company = connection.execute(
            """
            SELECT id
            FROM company_favourite
            WHERE user_id = ? AND company_id = ?
            """,
            (session["user_id"], company_id)
        ).fetchone()

        is_favourite = saved_company is not None

    # 所有公司资料读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把公司开发游戏、发行游戏和收藏状态传给公司详情页面。Show the company details.
    return render_template(
        "company.html",
        company=company,
        developed_games=developed_games,
        published_games=published_games,
        is_favourite=is_favourite
    )