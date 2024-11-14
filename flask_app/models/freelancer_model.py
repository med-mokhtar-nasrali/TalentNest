from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models.user_model import User


class Freelancer:
    def __init__(self,data):
        self.id = data["id"]
        self.phone = data["phone"]
        self.about_me = data["about_me"]
        self.experience = data["experience"]
        self.skills = data["skills"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]


# this method is to insert freelancer additionl info into its table
    @classmethod
    def add_freelancer_info(cls,data):
        query="insert into freelancers (phone, about_me, experience, skills, user_id) values (%(phone)s, %(about_me)s, %(experience)s, %(skills)s,%(user_id)s);"    
        return connectToMySQL( DB ).query_db(query,data)
    
