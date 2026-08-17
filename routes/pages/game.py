from flask import Blueprint, render_template, request, abort, session
import sqlite3


# 创建游戏页面的蓝图，游戏列表和游戏详情路由都会放在这里。Game pages blueprint.
game_bp = Blueprint("game", __name__)


@game_bp.route("/all")
def all_games():
    # 获取搜索框内容，去掉前后空格，再限制为最多100个字符。Clean the search text.
    search = request.args.get("search", "").strip()
    search = search[:100]

    # 连接数据库，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 如果搜索框为空，就读取数据库里的全部游戏，并按照游戏ID排列。Get all games.
    if search == "":
        games = connection.execute(
            """
            SELECT id, name, release_date, genre, cover, banner
            FROM game
            ORDER BY id
            """
        ).fetchall()

    # 如果用户输入了文字，就查找名称中包含这些文字的游戏。Search by game name.
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

    # 游戏数据读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把搜索结果和处理后的搜索文字传给All Games页面显示。Show the game list.
    return render_template(
        "all.html",
        games=games,
        search=search
    )


@game_bp.route("/game/<int:game_id>")
def game_detail(game_id):
    # 打开数据库并设置查询格式，准备读取这个游戏的详细资料。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 使用网页地址中的游戏ID查找对应的游戏。Find the selected game.
    game = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        WHERE id = ?
        """,
        (game_id,)
    ).fetchone()

    # 如果数据库里没有这个游戏ID，就关闭连接并显示404页面。Show 404 if not found.
    if game is None:
        connection.close()
        abort(404)

    # 从关联表中查找所有开发过这个游戏的公司。Get the developers.
    developers = connection.execute(
        """
        SELECT company.id, company.name, company.started
        FROM company
        JOIN game_developer
        ON company.id = game_developer.company_id
        WHERE game_developer.game_id = ?
        ORDER BY company.name
        """,
        (game_id,)
    ).fetchall()

    # 从关联表中查找所有发行过这个游戏的公司。Get the publishers.
    publishers = connection.execute(
        """
        SELECT company.id, company.name, company.started
        FROM company
        JOIN game_publisher
        ON company.id = game_publisher.company_id
        WHERE game_publisher.game_id = ?
        ORDER BY company.name
        """,
        (game_id,)
    ).fetchall()

    # 默认设置为没有收藏，因为未登录用户没有自己的收藏记录。Set the default status.
    is_favourite = False

    # 只有用户登录后，才记录浏览历史并检查这个游戏是否被收藏。Check the logged-in user.
    if session.get("user_id") is not None:
        # 加入用户浏览历史，OR IGNORE可以防止相同用户重复记录同一个游戏。Save the browsing history.
        connection.execute(
            """
            INSERT OR IGNORE INTO browsing_history (user_id, game_id)
            VALUES (?, ?)
            """,
            (session["user_id"], game_id)
        )

        connection.commit()

        # 在当前用户自己的收藏记录中查找这个游戏。Check this user's favourites.
        saved_game = connection.execute(
            """
            SELECT id
            FROM favourite
            WHERE user_id = ? AND game_id = ?
            """,
            (session["user_id"], game_id)
        ).fetchone()

        is_favourite = saved_game is not None

    # 所有游戏资料读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把游戏、开发公司、发行公司和收藏状态传给游戏详情页面。Show the game details.
    return render_template(
        "game.html",
        game=game,
        developers=developers,
        publishers=publishers,
        is_favourite=is_favourite
    )