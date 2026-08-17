from flask import Blueprint, render_template
import sqlite3


# 创建网站主页使用的蓝图。Home page blueprint.
home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    # 连接数据库，开启外键检查，并让查询结果可以使用字段名称读取。Open the database.
    connection = sqlite3.connect("database/app.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row

    # 按照游戏ID读取前三个游戏，用来显示主页的游戏介绍区域。Get the featured games.
    games = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY id
        LIMIT 3
        """
    ).fetchall()

    # 主页需要的游戏资料读取完成后关闭数据库连接。Close the database.
    connection.close()

    # 把三个游戏传给主页模板显示。Show the home page.
    return render_template(
        "home.html",
        games=games
    )