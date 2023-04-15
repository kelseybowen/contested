from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import contest, item
from flask_app.controllers import users_controller, ratings_controller, items_controller

@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        session["contest_name"] = ""
        session["contest_description"] = ""
        all_contests = contest.Contest.get_all_contests()
        return render_template("dashboard.html", all_contests=all_contests)
    else:
        return redirect('/')

@app.route('/contests/save', methods=["POST"])
def save_contest():
    if "user_id" in session:
        data = {
            "name": request.form["contest_name"],
            "description": request.form["contest_description"],
            "user_id": session["user_id"]
        }
        if not contest.Contest.validate_contest(data):
            session["contest_name"] = data["name"]
            session["contest_description"] = data["description"]
            return redirect("/dashboard")
        else:
            contest.Contest.save_contest(data)
            session["contest_name"] = ""
            session["contest_description"] = ""
            return redirect("/dashboard")
    else:
        return redirect('/')

@app.route('/contests/<int:contest_id>/edit')
def edit_contest(contest_id):
    if "user_id" in session:
        return render_template("edit_contest.html", edit_contest=contest.Contest.get_one_contest(contest_id), contest=contest.Contest.get_one_contest(contest_id), items=item.Item.get_all_items_in_single_contest(contest_id))
    else:
        return redirect("/")
    
@app.route('/contests/<int:contest_id>/update', methods=["POST"])
def update_contest(contest_id):
    if "user_id" in session:
        data = {
            "name": request.form["contest_name"],
            "description": request.form["contest_description"],
            "id": contest_id
        }
        if not contest.Contest.validate_contest(data):
            session["contest_name"] = data["name"]
            session["contest_description"] = data["description"]
            return redirect(f"/contests/{contest_id}/edit")
        else:
            contest.Contest.update_contest(data)
            session["contest_name"] = ""
            session["contest_description"] = ""
            return redirect(f"/contests/{contest_id}/items")
    else:
        return redirect('/')
    
@app.route('/contests/<int:contest_id>/close')
def close_contest(contest_id):
    if "user_id" in session:
        data = {
            "isOpen": 0,
            "id": contest_id
        }
        con = contest.Contest.get_one_contest(contest_id)
        if session["user_id"] == con["user_id"]:
            contest.Contest.change_contest_status(data)
            return redirect(f'/contests/{contest_id}/items')
        else:
            return "404 Error"
    else:
        return redirect('/')

@app.route('/contests/<int:contest_id>/open')
def open_contest(contest_id):
    if "user_id" in session:
        data = {
            "isOpen": 1,
            "id": contest_id
        }
        con = contest.Contest.get_one_contest(contest_id)
        if session["user_id"] == con["user_id"]:
            contest.Contest.change_contest_status(data)
            return redirect(f'/contests/{contest_id}/items')
        else:
            return "404 Error"
    else:
        return redirect('/')

@app.route('/contests/<int:contest_id>/delete')
def delete_contest(contest_id):
    if "user_id" in session:
        contest.Contest.delete_contest(contest_id)
        return redirect('/dashboard')
    else:
        return redirect('/')