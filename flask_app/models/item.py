from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash

class Item:
    db = "ratings_db"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.contest_id = data['contest_id']
        
    @classmethod
    def get_all_items(cls):
        query = "SELECT * FROM items;"
        results = connectToMySQL(cls.db).query_db(query)
        items = []
        for item in results:
            items.append(item)
        return items
        
    @classmethod
    def get_all_items_in_single_contest(cls, data):
        query = "SELECT * FROM items JOIN users ON users.id = items.user_id WHERE contest_id = %(contest_id)s;"
        data = {
            "contest_id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        items = []
        for entry in result:
            items.append(entry)
        return items
    
    @classmethod
    def get_one_item(cls, data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        return cls(result[0])
    
    @classmethod
    def save_item(cls, data):
        query = "INSERT INTO items (name, description, created_at, updated_at, user_id, contest_id) VALUES (%(name)s, %(description)s, NOW(), NOW(), %(user_id)s, %(contest_id)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_item(cls, data):
        query = "UPDATE items SET name=%(name)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete_item(cls,data):
        query = "DELETE FROM items WHERE id=%(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @staticmethod
    def validate_item(data):
        item_valid = True
        if len(data['name']) < 3:
            flash("Entry Name must be at least 3 characters", 'item')
            item_valid = False
        if not data['description']:
            flash("Description is required", 'item')
            item_valid = False
        return item_valid