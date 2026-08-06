from flask import Blueprint, render_template
import sqlite3


recommendation_bp = Blueprint("recommendation", __name__)


@recommendation_bp.route("/recommendation")
def recommendation():
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    game = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        ORDER BY RANDOM()
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    return render_template(
        "recommendation.html",
        game=game
    )