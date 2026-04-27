from flask import Flask, render_template, redirect, url_for, request
from flask_login import logout_user, login_user, login_required, LoginManager, current_user
from UserLogin import UserLogin
from db import *
from auth import *

init_db()

app = Flask(__name__)
app.secret_key = "secretsecretsecretsecret"

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/")
@app.route("/home")
def home():
    roadmaps = get_roadmaps()
    fav_ids = []

    if current_user.is_authenticated:
        fav_ids = get_fav_ids(current_user.id)

    return render_template('home.html', roadmaps=roadmaps, fav_ids=fav_ids, active_page="home")

@app.route("/register", methods=["GET", "POST"])
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

        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        user = get_user_by_login(username)

        if user and check_password_hash(user["password_hash"], password):
            user_obj = UserLogin().from_db(user)
            login_user(user_obj)

            next_page = request.args.get("next")

            return redirect(url_for("favorites"))
        
    return render_template("login.html")

@app.route("/favorites")
@login_required
def favorites():
    fav_ids = get_fav_ids(current_user.id)
    roadmaps = get_roadmaps()
    favs_roadmaps = [roadmap for roadmap in roadmaps if roadmap['id'] in fav_ids]
    return render_template("favorites.html", active_page="favorites", roadmaps=favs_roadmaps)

@app.route("/roadmap/<int:roadmap_id>")
def roadmap(roadmap_id):
    roadmap = get_roadmap_by_id(roadmap_id)
    steps = get_steps_by_roadmap_id(roadmap_id)
    user_steps = False
    is_fav = False
    if current_user.is_authenticated:    
        user_steps = get_user_steps(current_user.id, roadmap_id)
        is_fav = bool(get_fav(current_user.id, roadmap_id))

    if not roadmap or not steps:
        return redirect(url_for("home"))
    return render_template("roadmap.html", roadmap=roadmap, steps=steps, user_steps=user_steps, is_fav=is_fav)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/toggle-favorite/<int:roadmap_id>", methods=["POST"])
@login_required
def toggle_favorite(roadmap_id):
    user_id = current_user.id
    fav_ids = get_fav_ids(user_id)

    if roadmap_id in fav_ids:
        remove_fav(user_id, roadmap_id)
        remove_user_steps(user_id, roadmap_id)
    else:
        add_fav(user_id, roadmap_id)

    return '', 200

@app.route("/step/<int:step_id>/<string:status>", methods=["POST"])
@login_required
def update_step_status(step_id, status):
    update_user_step(current_user.id, step_id, status)
    return '', 200

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return UserLogin().from_db(user)
    return None


if __name__ == '__main__':  
    app.run(debug=True, port=8080)
