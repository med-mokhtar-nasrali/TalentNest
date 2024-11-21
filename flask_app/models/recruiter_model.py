from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models import user_model



class Recruiter:
    def __init__(self,data):
        self.id = data["id"]
        self.phone = data["phone"]
        self.about_me = data["about_me"]
        self.company_name= data["company_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.posted_by = user_model.User.get_user_by_id({'id':self.user_id})

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
                JOIN users ON recruiters.user_id = users.id
                WHERE recruiters.id = %(id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        recruiter = cls(result[0])
        return recruiter
    @classmethod
    def get_by_user_id(cls,data):
        query = """
                SELECT * FROM recruiters
                JOIN users ON recruiters.user_id = users.id
                WHERE recruiters.user_id = %(user_id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        recruiter = cls(result[0])
        return recruiter
    
    @classmethod
    def get_all_recruiters(cls):
        query = """
                SELECT * FROM recruiters;
                """
        result = connectToMySQL( DB ).query_db(query)
        all_recruiters=[]
        for row in result:
            all_recruiters.append(cls(row))
        return all_recruiters

    @classmethod
    def get_all_recruiters_profile(cls,data):
        query = """
                SELECT * FROM recruiters WHERE user_id=%(user_id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        return result[0]

    @classmethod
    def give_rating(cls,data):
        query="""
                INSERT INTO reviews (recruiter_id,freelancer_id,stars,content)
                VALUES (%(recruiter_id)s,%(freelancer_id)s,%(stars)s,%(contents)s)
                """
        result = connectToMySQL( DB ).query_db(query,data)
        return result


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