from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models.user_model import User
from flask_app.models.recruiter_model import Recruiter
from flask_app.models.freelancer_model import Freelancer


class Job:
    def __init__(self,data):
        self.id = data["id"]
        self.title = data["title"]
        self.required_tech = data["required_tech"]
        self.budget=data['budget']
        self.deadline= data["deadline"]
        self.description=data['description']
        self.category=data['category']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recruiter_id = data["recruiter_id"]
    

    @classmethod
    def add_job(cls,data):
        query="insert into jobs (title, required_tech, budget, deadline, description, category, recruiter_id) values (%(title)s, %(required_tech)s, %(budget)s,%(deadline)s,%(description)s ,%(category)s,%(recruiter_id)s);"  
        return connectToMySQL( DB ).query_db(query,data)
    
    @classmethod
    def show_all_jobs(cls):
        print('/'*30)
        print('before the querry')
        query=" select * from jobs ; "
        print('after the querry')
        results=connectToMySQL(DB).query_db(query)
        all_jobs=[]
        for row in results :
            job=cls(row)
            all_jobs.append(job)
        print (all_jobs)    
        return all_jobs    
        



    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["title"])<3:
            is_valid = False
            flash("title is too short","title")

        if len(data["required_tech"])<1:
            is_valid = False
            flash("Required Tech can not be empty","required_tech ")

        if len(data["budget"])<3:
            is_valid = False
            flash("Budget can not be empty","budget")

        if len(data["deadline"])<3:
            is_valid = False
            flash("Deadline can not be empty","deadline")
        if len(data["description"])<3:
            is_valid = False
            flash("description can not be empty","description")
                

        return is_valid    
