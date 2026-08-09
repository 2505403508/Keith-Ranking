from flask import Blueprint, render_template, request, abort, session
import sqlite3


pd_bp = Blueprint("pd", __name__)


@pd_bp.route("/pd")
def all_companies():
    search = request.args.get("search", "")

    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    if search == "":
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
            ORDER BY company.name
            """
        ).fetchall()

    else:
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
            WHERE company.name LIKE ?
            ORDER BY company.name
            """,
            ("%" + search + "%",)
        ).fetchall()

    connection.close()

    return render_template(
        "pd.html",
        companies=companies,
        search=search
    )


@pd_bp.route("/company/<int:company_id>")
def company_detail(company_id):
    connection = sqlite3.connect("database/app.db")
    connection.row_factory = sqlite3.Row

    company = connection.execute(
        """
        SELECT id, name, started
        FROM company
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    if company is None:
        connection.close()
        abort(404)

    developed_games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN game_developer
        ON game.id = game_developer.game_id

        WHERE game_developer.company_id = ?
        ORDER BY game.id
        """,
        (company_id,)
    ).fetchall()

    published_games = connection.execute(
        """
        SELECT
            game.id,
            game.name,
            game.release_date,
            game.genre,
            game.cover

        FROM game
        JOIN game_publisher
        ON game.id = game_publisher.game_id

        WHERE game_publisher.company_id = ?
        ORDER BY game.id
        """,
        (company_id,)
    ).fetchall()

    is_favourite = False

    if session.get("user_id") is not None:
        saved_company = connection.execute(
            """
            SELECT id
            FROM company_favourite
            WHERE user_id = ? AND company_id = ?
            """,
            (session["user_id"], company_id)
        ).fetchone()

        is_favourite = saved_company is not None

    connection.close()

    return render_template(
        "company.html",
        company=company,
        developed_games=developed_games,
        published_games=published_games,
        is_favourite=is_favourite
    )