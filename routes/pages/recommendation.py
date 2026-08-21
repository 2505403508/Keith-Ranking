from flask import Blueprint, render_template, redirect, session
import sqlite3


# 创建推荐功能的蓝图，随机推荐、个人推荐和清除历史都放在这里。Recommendation blueprint.
recommendation_bp = Blueprint("recommendation", __name__)


# 建立数据库连接，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
def get_connection():
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    return connection


@recommendation_bp.route("/recommendation")
def recommendation():
    # 打开数据库，准备从全部游戏中随机选择一个。Open the database.
    connection = get_connection()

    # 使用RANDOM随机排列游戏，并且只取第一条结果。Choose one random game.
    game = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY RANDOM()
        LIMIT 1
        """
    ).fetchone()

    # 随机游戏读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把随机游戏传给推荐页面，并说明这次使用的是随机推荐。Show the random recommendation.
    return render_template(
        "recommendation.html",
        game=game,
        recommendation_type="random",
        favourite_genre=None,
        history_count=0
    )


@recommendation_bp.route("/recommendation/personal")
def personal_recommendation():
    # 如果用户没有登录，就不能读取个人历史，并会被送到登录页面。Require login.
    if session.get("user_id") is None:
        return redirect("/login")

    # 打开数据库，准备读取当前用户自己的浏览历史。Open the database.
    connection = get_connection()

    # 计算当前用户浏览过多少个不同游戏，因为同一个游戏在历史中只会保存一次。Count the browsing history.
    history_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM browsing_history
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    # 按照genre分组并计算数量，数量最多的完整genre会成为用户最常浏览的类型。Find the favourite genre.
    favourite_genre = connection.execute(
        """
        SELECT
            game.genre,
            COUNT(*) AS genre_count

        FROM browsing_history
        JOIN game
        ON browsing_history.game_id = game.id

        WHERE browsing_history.user_id = ?
        GROUP BY game.genre

        ORDER BY genre_count DESC
        LIMIT 1
        """,
        (session["user_id"],)
    ).fetchone()

    # 默认没有推荐结果，后面的查询找到游戏后会替换这个值。Set an empty result.
    game = None

    # 只有用户有浏览历史时，才根据最常浏览的genre查找游戏。Use the browsing history.
    if favourite_genre is not None:
        # 从用户最常浏览的genre中随机选择一个没有浏览过的游戏。Recommend an unviewed game.
        game = connection.execute(
            """
            SELECT id, name, release_date, genre, cover, banner
            FROM game

            WHERE genre = ?
            AND id NOT IN (
                SELECT game_id
                FROM browsing_history
                WHERE user_id = ?
            )

            ORDER BY RANDOM()
            LIMIT 1
            """,
            (
                favourite_genre["genre"],
                session["user_id"]
            )
        ).fetchone()

        # 如果这个genre没有未浏览游戏，就从其他所有未浏览游戏中随机选择一个。Use the fallback.
        if game is None:
            game = connection.execute(
                """
                SELECT id, name, release_date, genre, cover, banner
                FROM game

                WHERE id NOT IN (
                    SELECT game_id
                    FROM browsing_history
                    WHERE user_id = ?
                )

                ORDER BY RANDOM()
                LIMIT 1
                """,
                (session["user_id"],)
            ).fetchone()

    # 推荐查询完成后关闭数据库连接。Close the database.
    connection.close()

    # 把推荐结果、最常浏览的genre和历史数量传给推荐页面。Show the personal recommendation.
    return render_template(
        "recommendation.html",
        game=game,
        recommendation_type="personal",
        favourite_genre=(
            favourite_genre["genre"]
            if favourite_genre is not None
            else None
        ),
        history_count=history_count
    )


@recommendation_bp.route(
    "/recommendation/history/clear",
    methods=["POST"]
)
def clear_recommendation_history():
    # 如果用户没有登录，就不能清除任何浏览历史，并会被送到登录页面。Require login.
    if session.get("user_id") is None:
        return redirect("/login")

    # 打开数据库准备删除当前用户自己的历史记录。Open the database.
    connection = get_connection()

    # 只删除session中这个用户的浏览历史，不会删除其他用户的记录。Clear this user's history.
    connection.execute(
        """
        DELETE FROM browsing_history
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    # 保存删除结果并关闭数据库连接。Save the change.
    connection.commit()
    connection.close()

    # 清除完成后返回个人推荐页面，页面会显示没有浏览历史的状态。Return to the personal page.
    return redirect("/recommendation/personal")