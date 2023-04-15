from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import item, contest
import math

@app.route('/contests/<int:contest_id>/items')
def view_contest_items(contest_id):
    if "user_id" in session:
        contest_info = contest.Contest.get_one_contest(contest_id)
        if contest_info:
            contest_items = item.Item.get_all_items_in_single_contest(contest_id)
        else:
            return redirect('/dashboard')
        
        if not contest_items:
            return render_template("contest_detail.html", contest=contest_info)
        if contest_info["isOpen"]:
            return render_template("contest_detail.html", items=contest_items, contest=contest_info)
        else:
            for result in contest_items:
                data = {
                    "contest_id": contest_id,
                    "item_id": result["id"]
                }
                result["average"] = math.ceil(item.Item.get_average_rating_for_item(data)*100)/100
            items = sorted(contest_items, key=lambda i: i["average"], reverse=True)
            return render_template("contest_results.html", contest=contest_info, items=items)
    else:
        return redirect("/")
    
@app.route('/contests/<int:contest_id>/items/new', methods=["POST"])
def add_item_to_contest(contest_id):
    if "user_id" in session:
        data = {
            "name": request.form["item_name"],
            "description": request.form["item_description"],
            "owner_id": session["user_id"],
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

    
@app.route('/contests/<int:contest_id>/items/<int:id>')
def edit_item(contest_id, id):
    if "user_id" in session:
        item1 = item.Item.get_one_item(id)
        contest_info = contest.Contest.get_one_contest(contest_id)
        contest_items = item.Item.get_all_items_in_single_contest(contest_id)
        return render_template("edit_item.html", edit_item=item1, contest=contest_info, items=contest_items)    
    else:
        return redirect("/")

@app.route('/contests/<int:contest_id>/items/<int:id>/update', methods=["POST"])
def update_item(contest_id, id):
    if "user_id" in session:
        data = {
            "name": request.form["item_name"],
            "description": request.form["item_description"],
            "id": id
        }
        if not item.Item.validate_item(data):
            session["item_name"] = data["name"]
            session["item_description"] = data["description"]
            return redirect(f"/contests/{contest_id}/items/{id}")
        else:
            item.Item.update_item(data)
            session["item_name"] = ""
            session["item_description"] = ""
            return redirect(f"/contests/{contest_id}/items")
            
@app.route('/contests/<int:contest_id>/items/<int:id>/delete')
def delete_item(id, contest_id):
    if "user_id" in session:
        item.Item.delete_item(id)
        return redirect(f'/contests/{contest_id}/items')
    else:
        return redirect('/')
