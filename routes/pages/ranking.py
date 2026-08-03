from flask import Blueprint, render_template, request
import sqlite3


ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/ranking")
def ranking():
    search = request.args.get("search", "")

    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    top_games = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY id
        LIMIT 3
        """
    ).fetchall()

    if search == "":
        games = connection.execute(
            """
            SELECT id, name, release_date, genre, cover, banner
            FROM game
            ORDER BY id
            """
        ).fetchall()
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

    connection.close()

    return render_template(
        "ranking.html",
        top_games=top_games,
        games=games,
        search=search
    )