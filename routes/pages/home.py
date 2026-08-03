from flask import Blueprint, render_template
import sqlite3


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    games = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY id
        LIMIT 3
        """
    ).fetchall()

    connection.close()

    return render_template(
        "home.html",
        games=games
    )