from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, session, redirect, render_template, url_for
from db import get_db

EMPTY_LOGIN_ERROR = "Вы не ввели логин!"
CONFIRM_PASSWORD_ERROR = "Пароли не совпадают!"
EMPTY_PASSWORD_ERROR = "Пароль не может быть пустым!"


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if (username == ''):
            return render_template("register.html", error=EMPTY_LOGIN_ERROR, is_active=True)

        if (password == ''):
            return render_template("register.html", error=EMPTY_PASSWORD_ERROR, is_active=True)


        if password == confirm_password:
            password_hash = generate_password_hash(password, method="pbkdf2:sha256")

            db = get_db()
            db.execute("""
                INSERT INTO users (username, password_hash) VALUES(?, ?)
                """, (username, password_hash))       
        
            

            db.commit()
            db.close()

            return redirect(url_for("auth.login"))
        else:
            return render_template("register.html", error=CONFIRM_PASSWORD_ERROR, is_active=True) 
    
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