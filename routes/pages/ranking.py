from flask import Blueprint, render_template, request

ranking_bp = Blueprint('ranking', __name__)
@ranking_bp.route('/ranking')
def ranking():
    return render_template("ranking.html")