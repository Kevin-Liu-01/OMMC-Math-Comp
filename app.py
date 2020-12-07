from flask import Flask, render_template, request
from flask_login import login_user, LoginManager
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_seasurf import SeaSurf
from user import User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.cfg")

    from routes.auth import auth
    app.register_blueprint(auth)

    from routes.main import main
    app.register_blueprint(main)

    @app.errorhandler(403)
    def does_not_exist(err):
        return render_template(
            "errors/client.html",
            title="403 Forbidden",
            message="You do not have access to this page."
        ), 403

    @app.errorhandler(404)
    def does_not_exist(err):
        return render_template(
            "errors/client.html",
            title="404 Not Found",
            message="Page not found."
        ), 404

    @app.errorhandler(500)
    def does_not_exist(err):
        return render_template("errors/error.html", title="500 Server Error"), 500

    login_manager = LoginManager()
    login_manager.session_protection = "strong"
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username: str):
        return User(username, True)

    limiter = Limiter(app, key_func=get_remote_address, default_limits=["1 per second"])

    @limiter.request_filter
    def ip_whitelist():
        return request.remote_addr == "127.0.0.1"

    SeaSurf(app)
    return app

create_app().run(port=3000)
