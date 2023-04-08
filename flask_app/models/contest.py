from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash


class Contest:
    db = "ratings_db"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def get_all_contests(cls):
        query = "SELECT * FROM contests;"
        results = connectToMySQL(cls.db).query_db(query)
        contests = []
        for contest in results:
            contests.append(cls(contest))
        return contests
    
    @classmethod            # basic contest info
    def get_one_contest(cls, data):
        # query = "SELECT * FROM contests JOIN users ON contests.user_id = users.id WHERE contests.id = %(id)s;" 
        query = "SELECT * FROM contests WHERE id=%(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]
    
    @classmethod
    def save_contest(cls,data):
        query = "INSERT INTO contests (name, description, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_contest(cls,data):
        query = "UPDATE contests SET name=%(name)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_contest(cls,data):
        query = "DELETE FROM contests WHERE id=%(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @staticmethod
    def validate_contest(data):
        contest_valid = True
        if len(data['name']) < 3:
            flash("Contest Name must be at least 3 characters", 'contest')
            contest_valid = False
        if not data['description']:
            flash("Description is required", 'contest')
            contest_valid = False
        return contest_valid