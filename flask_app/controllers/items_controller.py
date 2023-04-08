from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import item, contest
from flask_app.controllers import users_controller, contests_controller

@app.route('/contests/<int:contest_id>/items')
def view_contest_items(contest_id):
    if "user_id" in session:
        contest_info = contest.Contest.get_one_contest(contest_id)
        contest_items = item.Item.get_all_items_in_single_contest(contest_id)
        items = []
        for result in contest_items:
            items.append(result)
        return render_template("contest_detail.html", items=items, contest=contest_info)
        # return render_template("dashboard.html", items=items, contest=contest_info)
    else:
        return redirect("/")
    
@app.route('/contests/<int:contest_id>/items/new', methods=["POST"])
def add_items_to_contest(contest_id):
    if "user_id" in session:
        data = {
            "name": request.form["item_name"],
            "description": request.form["item_description"],
            "user_id": session["user_id"],
            "contest_id": contest_id
        }
        if not item.Item.validate_item(data):
            session["item_name"] = data["name"]
            session["item_description"] = data["description"]
            return redirect(f'/contests/{contest_id}/items')
        else:
            item.Item.save_item(data)
            session["item_name"] = ""
            session["item_description"] = ""
            return redirect(f'/contests/{contest_id}/items')
    else:
        return redirect('/')
            
@app.route('/contests/<int:contest_id>/items/<int:id>/delete')
def delete_item(id, contest_id):
    if "user_id" in session:
        item.Item.delete_item(id)
        return redirect(f'/contests/{contest_id}/items')
    else:
        return redirect('/')
