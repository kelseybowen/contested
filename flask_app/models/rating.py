from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Rating:
    db = "ratings_db"
    def __init__(self, data):
        self.id = data['id']
        self.score = data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.item_id = data['item_id']
    
    @classmethod
    def get_user_rating_for_item(cls, data):
        query = "SELECT * FROM ratings WHERE user_id = %(user_id)s AND item_id = %(item_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(f"RESULT FROM RATING.PY = {result}")
        if result:
            return result[0]
        else:
            return None
    
    @classmethod
    def get_all_user_ratings_for_contest(cls, data):
        query = "SELECT * FROM ratings JOIN items ON items.id = ratings.item_id WHERE ratings.user_id = %(user_id)s AND items.contest_id = %(contest_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
            
    
    @classmethod
    def save_rating(cls, data):
        query = "INSERT INTO ratings (score, user_id, item_id) VALUES (%(score)s, %(user_id)s, %(item_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_rating(cls, data):
        query = "UPDATE ratings SET score=%(score)s, updated_at=NOW() WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_rating(cls, data):
        query = "DELETE FROM ratings WHERE id=%(id)s;"
        data = {
            "id": data
        }
        print(data)
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @staticmethod
    def validate_rating(data):
        rating_valid = True
        if not (1 <= int(data) <= 10):
            flash("Rating must be between 1 and 10", 'rating')
            rating_valid = False
        return rating_valid
