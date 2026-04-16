from flask import Flask, render_template, request, redirect, session
from db import get_db, init_db
from auth import *

init_db()

app = Flask(__name__)
app.secret_key = "secretsecretsecretsecret"

app.register_blueprint(auth_bp)



@app.route('/home')
@app.route('/')
def home():
    db = get_db()
    all_roadmaps = db.execute("SELECT * FROM roadmaps").fetchall()
    db.close

    return render_template('home.html', roadmaps=all_roadmaps)

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':  
    app.run(debug=True, port=8080)


