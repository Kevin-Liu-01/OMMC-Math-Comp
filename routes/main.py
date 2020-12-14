from flask import Blueprint, render_template, abort
from flask_login import login_required
from markupsafe import escape
from user import User

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html", title="Home")

@main.route("/faq")
def about():
    return render_template("faq.html", title="FAQs")

@main.route("/user/<name>")
def profile(name: str):
    name = escape(name or "")
    user_object = User(name)

    if not user_object.exists:
        return abort(404)
    return render_template("profile.html", title=name, user=user_object)

@main.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="Settings")
