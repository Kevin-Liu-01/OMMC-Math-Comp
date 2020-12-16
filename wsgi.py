from flask import Flask, Response, render_template, request, redirect, url_for
from flask_limiter.util import get_remote_address
from flask_login import login_user, LoginManager
from sassutils.wsgi import SassMiddleware
from flask_limiter import Limiter
from flask_seasurf import SeaSurf
from data.user import User

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_pyfile("config.cfg")
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        f"{__name__}": ("static/sass", "static/css", "/static/css")
    })

    from routes.auth import auth
    app.register_blueprint(auth)

    from routes.main import main
    app.register_blueprint(main)

    @app.errorhandler(403)
    def does_not_exist(err):
        return render_template(
            "errors/client.html",
            code = "403",
            title = "403 Forbidden",
            message = "You do not have access to this page."
        ), 403

    @app.errorhandler(404)
    def does_not_exist(err):
        return render_template(
            "errors/client.html",
            code = "404",
            title = "404 Not Found",
            message = "Page not found."
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
