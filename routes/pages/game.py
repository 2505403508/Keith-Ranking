from flask import Blueprint, render_template, request

game_bp = Blueprint('game', __name__)

@game_bp.route('/game/')
def game():
    return render_template("game.html")