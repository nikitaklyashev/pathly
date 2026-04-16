from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, session, redirect, render_template, url_for
from password_strength import PasswordPolicy
from db import get_db


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        result = validate_login(username)
        if result != "SUCCESS":
            return render_template("register.html", error=result, is_active=True)
         
        result = validate_password(password, confirm_password) 
        if result != "SUCCESS":
            return render_template("register.html", error=result, is_active=True)
    
        password_hash = generate_password_hash(password, method="pbkdf2:sha256")

        db = get_db()
        db.execute("""
            INSERT INTO users (username, password_hash) VALUES(?, ?)
            """, (username, password_hash))       
    
        db.commit()
        db.close()

        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("auth.dashboard"))
    return render_template("login.html")

@auth_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def validate_password(password, confirm_password):
    CONFIRM_PASSWORD_ERROR = "Пароли не совпадают!"
    EMPTY_PASSWORD_ERROR = "Пароль не может быть пустым!"
    PASSWORD_STRENGTH_ERROR = "Пароль должен быть длиной не менее 8 символов, включать заглавную букву и цифру!"

    if not password:
        return EMPTY_PASSWORD_ERROR

    if password != confirm_password:
        return CONFIRM_PASSWORD_ERROR


    policy = PasswordPolicy.from_names(
        length=8,
        numbers=1,
        uppercase=1,
    )
    
    result = policy.test(password)

    if result:
        return PASSWORD_STRENGTH_ERROR
    
    return "SUCCESS"


def validate_login(login): 
    EMPTY_LOGIN_ERROR = "Вы не ввели логин!"
    LENGTH_LOGIN_ERROR = "Логин должен быть длиной не менее 4 символов!"

    if not login:
        return EMPTY_LOGIN_ERROR

    if len(login) < 4:
        return LENGTH_LOGIN_ERROR

    return "SUCCESS"
    
