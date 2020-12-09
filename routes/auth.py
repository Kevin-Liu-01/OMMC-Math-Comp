import hashlib, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from validate_email import validate_email
from markupsafe import escape
from name import Checker
from user import User

auth = Blueprint("auth", __name__)
hash_password = lambda p : hashlib.sha3_384(p.encode()).hexdigest()

def check_password(user_object, password: str):
    if not user_object.exists:
        return False

    return user_object["password"] == hash_password(password)

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
    user_object = User(username)

    if assertConditions(user_object, request.form.get("remember", True), zip(
        [
            request.form.get("g-recaptcha-response", False),
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
    user_object = User(username)

    if assertConditions(user_object, request.form.get("remember", True), zip(
        [
            request.form.get("g-recaptcha-response", False),
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
            email = email,
            bio = "No bio set.",
            followers = [],
            following = [],
            password = hash_password(password),
            created_date = datetime.datetime.now(),
            image_url = "https://cdn.pixabay.com/photo/2017/11/10/05/48/user-2935527_1280.png",
        )

        return redirect(url_for("main.home"))
    else:
        return render_template("auth/signup.html", title="Sign Up", email=email, username=username, password=password)

@auth.route("/logout")
@login_required
def logout():
    current_user.authenticated = False
    logout_user()

    return redirect(url_for("main.home"))
