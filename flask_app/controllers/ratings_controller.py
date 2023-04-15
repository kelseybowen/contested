from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import item, contest, rating
from flask_app.controllers import users_controller, contests_controller, items_controller

@app.route('/contests/<int:contest_id>/items/<int:item_id>/rate', methods=["POST"])
def new_rating(item_id, contest_id):
    if "user_id" in session:
        data = {
            "score": request.form["score"],
            "user_id": session["user_id"],
            "item_id": item_id
        }
        if request.form['score'] and not rating.Rating.validate_rating(request.form["score"]):
            return redirect(f"/contests/{contest_id}/items")
        existing_rating = rating.Rating.get_user_rating_for_item(data)
        if existing_rating:
            data["id"] = existing_rating["id"]
            rating.Rating.update_rating(data)
        else:
            rating.Rating.save_rating(data)
        return redirect(f"/contests/{contest_id}/items")
    else:
        return redirect("/")

@app.route('/contests/<int:contest_id>/items/<int:item_id>/<int:rating_id>/delete')
def delete_rating(contest_id, item_id, rating_id):
    if "user_id" in session:
        rating.Rating.delete_rating(rating_id)
        return redirect(f'/contests/{contest_id}/items')
    else:
        return redirect('/')

