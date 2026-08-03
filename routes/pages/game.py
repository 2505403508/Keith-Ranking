from flask import Blueprint, render_template, request
import sqlite3


game_bp = Blueprint("game", __name__)


@game_bp.route("/all")
def all_games():
    search = request.args.get("search", "")

    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

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
        "all.html",
        games=games,
        search=search
    )


@game_bp.route("/game/<int:game_id>")
def game_detail(game_id):
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    game = connection.execute(
        """
        SELECT id, name, release_date, genre, cover, banner
        FROM game
        WHERE id = ?
        """,
        (game_id,)
    ).fetchone()

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

    connection.close()

    if game is None:
        return "Game not found", 404

    return render_template(
        "game.html",
        game=game,
        developers=developers,
        publishers=publishers
    )