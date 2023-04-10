from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, contest
from flask_app.controllers import users_controller

@app.route('/dashboard')
def dashboard():
    if "user_id" in session:
        session["name"] = ""
        session["description"] = ""
        all_contests = contest.Contest.get_all_contests()
        return render_template("dashboard.html", all_contests=all_contests)
    else:
        return redirect('/')
    
@app.route('/contests/new')
def add_contest():
    if "user_id" in session:
        return render_template("new_contest.html")
    else:
        return redirect('/')

@app.route('/contests/save', methods=["POST"])
def save_contest():
    if "user_id" in session:
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "user_id": session["user_id"]
        }
        if not contest.Contest.validate_contest(data):
            session["contest_name"] = data["name"]
            session["contest_description"] = data["description"]
            return redirect("/contests/new")
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
        return render_template("edit_contest.html", contest=contest.Contest.get_one_contest(contest_id))
    else:
        return redirect("/")

# @app.route('/contests/<int:contest_id>')
# def contest_detail(contest_id):
#     if "user_id" in session:
#         one_contest = contest.Contest.get_one_contest(contest_id)
#         print(one_contest)
#         return render_template("contest_detail.html", one_contest=one_contest)
#     else:
#         return redirect("/")

# @app.route('/contests/<int:contest_id>/show')
# def render_contest():
#     document.getElementByID
    
@app.route('/contests/<int:contest_id>/update', methods=["POST"])
def update_contest(contest_id):
    if "user_id" in session:
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
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
            return redirect("/dashboard")
    else:
        return redirect('/')


@app.route('/contests/<int:contest_id>/delete')
def delete_contest(contest_id):
    if "user_id" in session:
        # one_contest = contest.Contest.get_one_contest(contest_id)
        contest.Contest.delete_contest(contest_id)
        return redirect('/dashboard')
    else:
        return redirect('/')