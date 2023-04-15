from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import statistics

class Item:
    db = "ratings_db"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']
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
        query = "SELECT * FROM items AS i LEFT JOIN (SELECT * FROM ratings WHERE ratings.user_id = %(user_id)s) AS r ON i.id = r.item_id JOIN users AS u ON u.id = i.owner_id WHERE contest_id = %(contest_id)s;"
        data = {
            "contest_id": data,
            "user_id": session["user_id"]
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        items = []
        if result:
            for entry in result:
                items.append(entry)
            return items
        else:
            pass
    
    @classmethod
    def get_one_item(cls, data):
        query = "SELECT * FROM items WHERE id = %(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_average_rating_for_item(cls, data):
        query = "SELECT * FROM ratings JOIN items ON items.id = ratings.item_id WHERE contest_id = %(contest_id)s AND item_id = %(item_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        scores = []
        for item in result:
            scores.append(item["score"])
        if len(scores) < 1:
            return -1
        else:
            return statistics.mean(scores)
        
    
    @classmethod
    def save_item(cls, data):
        query = "INSERT INTO items (name, description, created_at, updated_at, owner_id, contest_id) VALUES (%(name)s, %(description)s, NOW(), NOW(), %(owner_id)s, %(contest_id)s);"
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