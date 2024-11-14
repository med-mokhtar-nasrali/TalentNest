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