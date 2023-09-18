from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import category
from flask_app.controllers import users_controller, contests_controller, items_controller

@app.route('/contests/<int:contest_id>/categories/new', methods=["POST"])
def new_category(contest_id):
    if "user_id" in session:
        data = {
            "title": request.form["category_title"],
            "description": request.form["category_description"],
            "contest_id": contest_id
        }
        category.Category.save_category(data)
    else:
        return redirect("/")