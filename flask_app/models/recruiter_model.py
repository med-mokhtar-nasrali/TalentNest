from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models.user_model import User



class Recruiter:
    def __init__(self,data):
        self.id = data["id"]
        self.phone = data["phone"]
        self.about_me = data["about_me"]
        self.company_name= data["company_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

#this method is to insert recuiter addional info into its table 
    @classmethod
    def add_recruiter_info(cls,data):
        query="insert into recruiters (phone, about_me, company_name, user_id) values (%(phone)s, %(about_me)s, %(company_name)s,%(user_id)s);"  
        return connectToMySQL( DB ).query_db(query,data)        
    
    @classmethod
    def update(cls,data):
        query = """
                UPDATE recruiters SET
                phone = %(phone)s,
                about_me = %(about_me)s,
                company_name = %(company_name)s
                WHERE recruiters.id = %(id)s;
                """
        return connectToMySQL( DB ).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM recruiters
                JOIN users ON recruiters.user_id = user_id
                WHERE recruiters.id = %(id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        recruiter = cls(result[0])
        recruiter.posted_by = f'{result[0]["first_name"]}{result[0]["last_name"]}'
        return recruiter


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["phone"])<8:
            is_valid = False
            flash("Phone number is too short","phone")
        if len(data["about_me"])<3:
            is_valid = False
            flash("About Me can't be empty","about_me")
        if len(data["company_name"])<1:
            is_valid = False
            flash("Company Name can't be empty ","company_name")
        return is_valid