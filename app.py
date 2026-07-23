from flask import Flask, render_template, request
from routes.pages.home import home_bp as home
from routes.pages.game import game_bp as game

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(game)

if __name__ == "__main__":
    app.run(debug=True)
