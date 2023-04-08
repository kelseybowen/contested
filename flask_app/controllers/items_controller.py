from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import item
from flask_app.controllers import users_controller

@app.route('/contests/<int:contest_id>/detail')
def view_contest_items(contest_id):
    if "user_id" in session:
        one_contest = item.Item.get_all_items_in_single_contest(contest_id)
        contest_items = []
        for result in one_contest:
            contest_items.append(result)
            # print(f"PRINTING FROM ITEMS_CONTROLLER = {result.name}")
        return render_template("contest_detail.html", contest=contest_items)
    else:
        return redirect("/")
