import os, requests, hashlib
from flask import Blueprint, render_template, abort, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from markupsafe import escape
from typing import Union
from name import Checker

from data.team import Team
from data.user import User

hash_password = lambda p : hashlib.sha3_384(p.encode()).hexdigest()

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

@main.route("/rules")
def rules():
    return render_template("rules.html", title="Rules")

@main.route("/info")
def info():
    return render_template("info.html", title="Info")

@main.route("/terms")
def terms():
    return render_template("terms.html", title="Terms")

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

    if not request.form.get("rules", False):
        session["open_join"] = True
        session["team_name"] = team_name

        flash("Please accept the rules.")
        return redirect(url_for("main.join"))

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

    if team_name == User(current_user.username)["team"]:
        session["open_join"] = True
        session["team_name"] = team_name

        flash("You are already a member of this team.")
        return redirect(url_for("main.join"))

    if team_object["join_code"] != hash_password(join_code):
        session["open_join"] = True
        session["team_name"] = team_name

        flash("Incorrect join code provided.")
        return redirect(url_for("main.join"))

    previous_team = Team(current_user["team"])
    previous_members = previous_team["members"]
    previous_members.remove(current_user.username)

    if len(previous_members) < 1 and previous_team.name != "Solo":
        previous_team.database.document(previous_team.name).delete()
    else:
        previous_team.update(members=previous_members or [])

    current_members = team_object["members"]
    current_members.append(current_user.username)

    team_object.update(members=current_members)
    current_user.update(team=team_name)

    session["team_name"] = ""
    session["open_join"] = False
    return redirect(f"/team/{team_name}")

@main.route("/create", methods=["POST"])
@login_required
def create():
    team_name = escape(request.form.get("name", "Solo"))
    password = escape(request.form.get("password", ""))
    captcha = request.form.get("g-recaptcha-response", False)

    if not request.form.get("rules", False):
        flash("Please accept the rules.")
        return render_template("join.html", title="Join Team", team_name=team_name, password=password, teams=Team("placeholder").database.stream())

    logCaptcha(captcha)
    if not captcha:
        flash("Please complete the reCAPTCHA.")
        return render_template("join.html", title="Join Team", team_name=team_name, password=password, teams=Team("placeholder").database.stream())

    if password == "":
        flash("Invalid password provided.")
        return render_template("join.html", title="Join Team", team_name=team_name, teams=Team("placeholder").database.stream())

    team_object = Team(team_name)
    if team_object.exists or team_object.name == "Solo":
        flash("Team name already in use.")
        return render_template("join.html", title="Join Team", password=password, teams=Team("placeholder").database.stream())

    if not Checker(team_name).is_valid:
        flash("Team name not allowed.")
        return render_template("join.html", title="Join Team", password=password, teams=Team("placeholder").database.stream())

    previous_team = Team(current_user["team"])
    previous_members = previous_team["members"]
    previous_members.remove(current_user.username)

    if len(previous_members) < 1 and previous_team.name != "Solo":
        previous_team.database.document(previous_team.name).delete()
    else:
        previous_team.update(members=previous_members or [])

    User(current_user.username).update(team=team_name)
    team_object.update(
        join_code = hash_password(password),
        members = [current_user.username],
        submitted = False,
    )

    session["team_name"] = ""
    session["open_join"] = False
    return redirect(f"/team/{team_name}")

@main.route("/settings")
@login_required
def settings():
    return render_template("settings.html", title="Settings")
