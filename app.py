from flask import Flask, render_template
from routes.pages.home import home_bp as home
from routes.pages.game import game_bp as game
from routes.pages.ranking import ranking_bp as ranking
from routes.pages.pd import pd_bp as pd
from routes.pages.recommendation import recommendation_bp as recommendation


app = Flask(__name__)


app.register_blueprint(home)
app.register_blueprint(game)
app.register_blueprint(ranking)
app.register_blueprint(pd)
app.register_blueprint(recommendation)


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        error_title="Page Not Found",
        error_message="The page you are looking for does not exist."
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message="Something went wrong while loading this page."
    ), 500


if __name__ == "__main__":
    app.run(debug=True)