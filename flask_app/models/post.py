from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
#email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# special_chars = ['$','&','!','%']

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


from flask_app.models import user

class Post:
    def __init__(self , data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.name = data['name']
        self.creator = None

    @staticmethod
    def validate_post(post):
        is_valid=True
        if len(post['content']) < 1:
            flash("Please Make A Longer Post !","post")
            is_valid = False
        return is_valid


    @classmethod
    def get_all_posts(cls):
        # Select all from posts and join them together via their ids
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL('recipes_assignment').query_db(query)
        print(results)
        all_posts = []
        for row in results:
            one_post = cls(row)
            one_post_author_info = {
                "id": row['users.id'],
                "content": row['content'],
                "created_at": row['created_at'],
                "first_name": row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "updated_at": row['updated_at'],
                "password": row['password'],
                "instructions": row['instructions'],
                "date_cooked": row['date_cooked'],
                "under_30": row['under_30'],
                "name": row['name']
            }
            author = user.User(one_post_author_info)
            one_post.creator = author
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def publish(cls,data):
        query = "INSERT INTO recipes_assignment.posts (content,created_at,updated_at,user_id,instructions, date_cooked,under_30,name) VALUES (%(content)s,NOW(),NOW(),%(user_id)s,%(instructions)s,%(date_cooked)s,%(under_30)s,%(name)s);"
        results = connectToMySQL("recipes_assignment").query_db(query,data)
        print(results)
        return results

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL("recipes_assignment").query_db(query,data)

    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM posts WHERE id = %(id)s;"
    #     return connectToMySQL('recipes_assignment').query_db(query,data)

    @classmethod
    def get_by_way_of_id(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL("recipes_assignment").query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE posts SET name=%(name)s,type=%(type)s,num_of_boxes=%(num_of_boxes)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes_assignment').query_db(query,data)

