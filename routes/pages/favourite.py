from flask import Blueprint, render_template, redirect, session, abort
import sqlite3


favourite_bp = Blueprint("favourite", __name__)


def get_connection():
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    return connection


@favourite_bp.route("/favourites")
def favourites():
    if session.get("user_id") is None:
        return redirect("/login")

    connection = get_connection()

    games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN favourite
        ON game.id = favourite.game_id

        WHERE favourite.user_id = ?
        ORDER BY game.id
        """,
        (session["user_id"],)
    ).fetchall()

    companies = connection.execute(
        """
        SELECT
            company.id,
            company.name,
            company.started,

            (
                SELECT COUNT(*)
                FROM game_developer
                WHERE game_developer.company_id = company.id
            ) AS developed_count,

            (
                SELECT COUNT(*)
                FROM game_publisher
                WHERE game_publisher.company_id = company.id
            ) AS published_count

        FROM company
        JOIN company_favourite
        ON company.id = company_favourite.company_id

        WHERE company_favourite.user_id = ?
        ORDER BY company.name
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "favourites.html",
        games=games,
        companies=companies
    )


@favourite_bp.route(
    "/favourite/game/<int:game_id>",
    methods=["POST"]
)
def favourite_game(game_id):
    if session.get("user_id") is None:
        return redirect("/login")

    connection = get_connection()

    game = connection.execute(
        """
        SELECT id
        FROM game
        WHERE id = ?
        """,
        (game_id,)
    ).fetchone()

    if game is None:
        connection.close()
        abort(404)

    saved_game = connection.execute(
        """
        SELECT id
        FROM favourite
        WHERE user_id = ? AND game_id = ?
        """,
        (session["user_id"], game_id)
    ).fetchone()

    if saved_game is None:
        connection.execute(
            """
            INSERT INTO favourite (user_id, game_id)
            VALUES (?, ?)
            """,
            (session["user_id"], game_id)
        )

    else:
        connection.execute(
            """
            DELETE FROM favourite
            WHERE user_id = ? AND game_id = ?
            """,
            (session["user_id"], game_id)
        )

    connection.commit()
    connection.close()

    return redirect("/game/" + str(game_id))


@favourite_bp.route(
    "/favourite/company/<int:company_id>",
    methods=["POST"]
)
def favourite_company(company_id):
    if session.get("user_id") is None:
        return redirect("/login")

    connection = get_connection()

    company = connection.execute(
        """
        SELECT id
        FROM company
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    if company is None:
        connection.close()
        abort(404)

    saved_company = connection.execute(
        """
        SELECT id
        FROM company_favourite
        WHERE user_id = ? AND company_id = ?
        """,
        (session["user_id"], company_id)
    ).fetchone()

    if saved_company is None:
        connection.execute(
            """
            INSERT INTO company_favourite (user_id, company_id)
            VALUES (?, ?)
            """,
            (session["user_id"], company_id)
        )

    else:
        connection.execute(
            """
            DELETE FROM company_favourite
            WHERE user_id = ? AND company_id = ?
            """,
            (session["user_id"], company_id)
        )

    connection.commit()
    connection.close()

    return redirect("/company/" + str(company_id))