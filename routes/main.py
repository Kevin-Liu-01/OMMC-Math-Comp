import os
from flask import Blueprint, render_template, send_from_directory, current_app, abort
from flask_login import login_required
from markupsafe import escape

from data.team import Team
from data.user import User

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html", title="Home")

@main.route("/faq")
def about():
    return render_template("faq.html", title="FAQs")

@main.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

@main.route("/user/<name>")
def user(name: str):
    name = escape(name or "")
    user_object = User(name)

    if not user_object.exists:
        return abort(404)
    return render_template("profile.html", title=name, user=user_object)

@main.route("/team/<name>")
def team(name: str):
    name = escape(name or "")
    team_object = Team(name)

    if not team_object.exists:
        return abort(404)
    return render_template("team.html", title=name, team=team_object)

@main.route("/participants")
def participants():
    return render_template(
        "participants.html",
        title="Participants",
        teams=Team("placeholder").database.stream()
    )

@main.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="Settings")
