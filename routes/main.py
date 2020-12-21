import os, requests
from flask import Blueprint, render_template, abort, redirect, url_for, request, flash
from flask_login import login_required, current_user
from markupsafe import escape
from typing import Union

from data.team import Team
from data.user import User

def logCaptcha(result: Union[str, bool]):
    if isinstance(result, bool):
        return

    try:
        requests.post("https://www.google.com/recaptcha/api/siteverify", data = {
            "secret": "6LeUQ_wZAAAAAPn3LFgBprWlUsjvextIQqY3FHnq",
            "remoteip": request.remote_addr,
            "response": result
        })
    except:
        pass

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html", title="Home")

@main.route("/home")
def redirect_home():
    return redirect(url_for("main.home"))

@main.route("/faq")
def about():
    return render_template("faq.html", title="FAQs")

@main.route("/creators")
def creators():
    return render_template("creators.html", title="Creators")

@main.route("/favicon.ico")
def favicon():
    from flask import send_from_directory, current_app

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

@main.route("/join", methods=["GET", "POST"])
@login_required
def join():
    from flask import session

    if request.method == "GET":
        return render_template(
            "join.html",
            title="Join Team",
            team_name = session.get("team_name", ""),
            open_join = session.get("open_join", False),
            teams=Team("placeholder").database.stream()
        )

    team_name = escape(request.form.get("team_name", ""))
    join_code = escape(request.form.get("join_code", ""))
    captcha = request.form.get("g-recaptcha-response", False)
    team_object = Team(team_name)

    logCaptcha(captcha)
    if not captcha:
        session["open_join"] = True
        session["team_name"] = team_name

        flash("Please complete the captcha.")
        return redirect(url_for("main.join"))

    if not team_object.exists:
        session["open_join"] = True
        session["team_name"] = team_name

        flash("Unable to get team object.")
        return redirect(url_for("main.join"))

    if team_object["join_code"] != join_code:
        session["open_join"] = True
        session["team_name"] = team_name

        flash("Incorrect join code provided.")
        return redirect(url_for("main.join"))

    for team in team_object.database.where("members", "array_contains", current_user.username).stream():
        existing_team = Team(team.id)
        existing_team.update(members=existing_team["members"].remove(current_user.username))

    current_members = team_object["members"]
    current_members.append(current_user.username)

    team_object.update(members=current_members)
    current_user.update(
        team = team_name
    )

    session["team_name"] = ""
    session["open_join"] = False
    return redirect(f"/team/{team_name}")

@auth.route("/create", methods=["POST"])
@login_required
def create():
    flash("This functionality is still undergoing testing.")
    return redirect(url_for("main.join"))

@main.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="Settings")
