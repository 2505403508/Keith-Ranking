from flask import Blueprint, render_template, redirect, session
import sqlite3


recommendation_bp = Blueprint("recommendation", __name__)


def get_connection():
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    return connection


@recommendation_bp.route("/recommendation")
def recommendation():
    connection = get_connection()

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
        game=game,
        recommendation_type="random",
        favourite_genre=None,
        history_count=0
    )


@recommendation_bp.route("/recommendation/personal")
def personal_recommendation():
    if session.get("user_id") is None:
        return redirect("/login")

    connection = get_connection()

    history_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM browsing_history
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

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

    game = None

    if favourite_genre is not None:
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

    connection.close()

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
    if session.get("user_id") is None:
        return redirect("/login")

    connection = get_connection()

    connection.execute(
        """
        DELETE FROM browsing_history
        WHERE user_id = ?
        """,
        (session["user_id"],)
    )

    connection.commit()
    connection.close()

    return redirect("/recommendation/personal")