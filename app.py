from flask import Flask, render_template
from routes.pages.home import home_bp as home
from routes.pages.game import game_bp as game
from routes.pages.ranking import ranking_bp as ranking
from routes.pages.pd import pd_bp as pd
from routes.pages.recommendation import recommendation_bp as recommendation
from routes.pages.signup import signup_bp as signup
from routes.pages.login import login_bp as login
from routes.pages.favourite import favourite_bp as favourite


# 创建Flask网站程序，所有页面都会从这个程序启动。Create the Flask app.
app = Flask(__name__)

# 设置session需要使用的密钥，让登录资料可以保存在用户的session中。Set the session key.
app.secret_key = "keith-ranking-secret-key-2026"

# 注册所有页面蓝图，让每个文件中的网址路由可以在网站中使用。Register the blueprints.
app.register_blueprint(home)
app.register_blueprint(game)
app.register_blueprint(ranking)
app.register_blueprint(pd)
app.register_blueprint(recommendation)
app.register_blueprint(signup)
app.register_blueprint(login)
app.register_blueprint(favourite)


# 当用户打开一个不存在的网址时，显示自定义404页面。Show the 404 page.
@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        error_title="Page Not Found",
        error_message="The page you are looking for does not exist."
    ), 404


# 当网站运行时发生服务器错误，显示自定义500页面。Show the 500 page.
@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message="Something went wrong while loading this page."
    ), 500


# 直接运行这个文件时启动Flask开发服务器。Start the development server.
if __name__ == "__main__":
    app.run(debug=True)