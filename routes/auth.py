import hashlib, datetime, requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from validate_email import validate_email
from markupsafe import escape
from typing import Union
from name import Checker

from data.user import User
from data.team import Team

auth = Blueprint("auth", __name__)
hash_password = lambda p : hashlib.sha3_384(p.encode()).hexdigest()

def check_password(user_object, password: str):
    if not user_object.exists:
        return False

    return user_object["password"] == hash_password(password)

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

def assertConditions(user_object, remember: bool, conditions):
    for condition, message in conditions:
        if condition:
            continue

        flash(message)
        return False

    user_object.authenticate()
    current_user.authenticated = True

    login_user(user_object, remember=remember)
    return True

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html", title="Login")

    username = escape(request.form.get("name", ""))
    password = escape(request.form.get("password", ""))
    captcha = request.form.get("g-recaptcha-response", False)
    user_object = User(username)

    logCaptcha(captcha)
    if assertConditions(user_object, request.form.get("remember", True), zip(
        [
            captcha,
            user_object.exists,
            check_password(user_object, password)
        ],
        ["Please complete the reCAPTCHA.", "Invalid username provided.", "Username or password is incorrect."]
    )):
        return redirect(url_for("main.home"))
    else:
        return render_template("auth/login.html", title="Login", username=username, password=password)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html", title="Sign Up")

    email = escape(request.form.get("email", ""))
    username = escape(request.form.get("name", ""))
    password = escape(request.form.get("password", ""))
    captcha = request.form.get("g-recaptcha-response", False)
    user_object = User(username)

    logCaptcha(captcha)
    if assertConditions(user_object, request.form.get("remember", True), zip(
        [
            captcha,
            not user_object.exists,
            Checker(username).is_valid,
            validate_email(email, check_regex=True, use_blacklist=True, check_mx=False, debug=False),
            len(list(user_object.database.where("email", "==", email).stream())) == 0
        ],
        ["Please complete the reCAPTCHA.", "Username is already in use.", "Username not allowed.", "Invalid email.", "Email is already in use."]
    )):
        user_object.update(
            points = 0,
            posts = [],
            team = "Solo",
            email = email,
            bio = "No bio set.",
            followers = [],
            following = [],
            submitted = False,
            password = hash_password(password),
            created_date = datetime.datetime.now(),
            image_url = "https://cdn.pixabay.com/photo/2017/11/10/05/48/user-2935527_1280.png",
        )

        solo_team = Team("Solo")
        current_members = solo_team["members"]
        current_members.append(username)

        solo_team.update(members=current_members)
        return redirect(url_for("main.home"))
    else:
        return render_template("auth/signup.html", title="Sign Up", email=email, username=username, password=password)

@auth.route("/logout")
@login_required
def logout():
    current_user.authenticated = False
    logout_user()

    return redirect(url_for("main.home"))
