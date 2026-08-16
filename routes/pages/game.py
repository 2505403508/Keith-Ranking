from flask import Blueprint, render_template, request, abort, session
import sqlite3


game_bp = Blueprint("game", __name__)


@game_bp.route("/all")
def all_games():
    search = request.args.get("search", "").strip()
    search = search[:100]

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

    if game is None:
        connection.close()
        abort(404)

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

    is_favourite = False

    if session.get("user_id") is not None:
        connection.execute(
            """
            INSERT OR IGNORE INTO browsing_history (user_id, game_id)
            VALUES (?, ?)
            """,
            (session["user_id"], game_id)
        )

        connection.commit()

        saved_game = connection.execute(
            """
            SELECT id
            FROM favourite
            WHERE user_id = ? AND game_id = ?
            """,
            (session["user_id"], game_id)
        ).fetchone()

        is_favourite = saved_game is not None

    connection.close()

    return render_template(
        "game.html",
        game=game,
        developers=developers,
        publishers=publishers,
        is_favourite=is_favourite
    )