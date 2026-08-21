from flask import Blueprint, render_template, request
import sqlite3


# 创建游戏排名页面使用的蓝图。Ranking blueprint.
ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/ranking")
def ranking():
    # 获取排名页搜索框内容，去掉前后空格，再限制为最多100个字符。Clean the search text.
    search = request.args.get("search", "").strip()
    search = search[:100]

    # 连接数据库，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 读取排名最前面的三个游戏，用来显示页面上方的前三名区域。Get the top three games.
    top_games = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY id
        LIMIT 3
        """
    ).fetchall()

    # 如果搜索框为空，就读取完整的游戏排名。Get the full ranking.
    if search == "":
        games = connection.execute(
            """
            SELECT id, name, release_date, genre, cover, banner
            FROM game
            ORDER BY id
            """
        ).fetchall()

    # 如果用户输入了文字，就查找名称中包含这些文字的排名游戏。Search the ranking.
    else:
        games = connection.execute(
            """
            SELECT id, name, release_date, genre, cover, banner
            FROM game
            WHERE name LIKE ?
            ORDER BY id
            """,
            ("%" + search + "%",)
        ).fetchall()

    # 排名数据读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把前三名完整结果和搜索内容传给排名页面。Show the ranking page.
    return render_template(
        "ranking.html",
        top_games=top_games,
        games=games,
        search=search
    )