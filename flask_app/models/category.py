from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Category:
    db = "ratings_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.contest_id = data['contest_id']
    
    @classmethod
    def get_all_categories_for_contest(cls, data):
        query = "SELECT * FROM categories WHERE contest_id = %(contest_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def save_category(cls, data):
        query = "INSERT INTO categories (title, description, contest_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(contest_id)s, NOW(), NOW());"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_category(cls, data):
        query = "UPDATE categories SET title=%(title)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_category(cls, data):
        query = "DELETE FROM categories WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @staticmethod
    def validate_category(data):
        category_valid = True
        if len(data['title'] < 3):
            flash("Title must be at least 3 characters", 'category')
            category_valid = False
        if len(data['description'] < 3):
            flash("Description must be at least 3 characters", 'category')
            category_valid = False
        return category_valid