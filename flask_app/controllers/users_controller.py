from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, contest
from flask_app.controllers import contests_controller
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    # session["index"] = "login"
    return render_template("index.html")

    
@app.route('/register', methods=["POST"])
def register():
    if not user.User.validate_registration(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['r_email']
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["r_email"],
        "password": bcrypt.generate_password_hash(request.form["r_password"])
    }
    user_id = user.User.save_user(data)
    session['user_id'] = user_id
    session['first_name'] = data["first_name"]
    return redirect('/dashboard')

    
@app.route('/login', methods=["POST"])
def login():
    user_in_db = user.User.get_user_by_email(request.form["l_email"])
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['l_password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')