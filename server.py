from flask_app import app
from flask_app.controllers import users_controller, contests_controller, items_controller

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
