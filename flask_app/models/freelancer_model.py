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
        self.education = data["education"]
        self.github = data["github"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.posted_by = ""

# this method is to insert freelancer additionl info into its table
    @classmethod
    def add_freelancer_info(cls,data):
        query="insert into freelancers (phone, about_me, experience, skills, education, github, user_id) values (%(phone)s, %(about_me)s, %(experience)s, %(skills)s, %(education)s, %(github)s,%(user_id)s);"    
        return connectToMySQL( DB ).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = """
                UPDATE freelancers SET
                phone = %(phone)s,
                about_me = %(about_me)s,
                experience = %(experience)s,
                skills = %(skills)s,
                education = %(education)s,
                github = %(github)s
                WHERE freelancers.id = %(id)s;
                """
        return connectToMySQL( DB ).query_db(query,data)
    

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM freelancers
                JOIN users ON freelancers.user_id = user_id
                WHERE freelancers.id = %(id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        freelancer = cls(result[0])
        freelancer.posted_by = f'{result[0]["first_name"]}{result[0]["last_name"]}'
        return freelancer

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["phone"])<8:
            is_valid = False
            flash("Phone number is too short","phone")
        if len(data["about_me"])<3:
            is_valid = False
            flash("About Me cant be empty","about_me")
        if len(data["experience"])<3:
            is_valid = False
            flash("Experience cant be empty","experience")
        if len(data["skills"])<3:
            is_valid = False
            flash("Skills cant be empty","skills")
        if len(data["education"])<3:
            is_valid = False
            flash("Education cant be empty","education")
        if len(data["github"])<3:
            is_valid = False
            flash("Github cant be empty","github")
        return is_valid