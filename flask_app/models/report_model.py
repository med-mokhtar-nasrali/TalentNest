from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash


class Report:
    def __init__(self,data):
        self.id = data["id"]
        self.sender_id = data["sender_id"]
        self.reported_id = data["reported_id"]
        self.reason = data["reason"]
        self.message = data["message"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #this method is to insert report 
    @classmethod
    def add_report(cls,data):
        query="INSERT INTO reports (sender_id,reported_id, message, reason) values (%(sender_id)s,%(reported_id)s, %(message)s,%(reason)s);"  
        return connectToMySQL( DB ).query_db(query,data)        
    

    @classmethod
    def show_all_reports(cls):
        query = "SELECT * FROM reports;"
        results=connectToMySQL(DB).query_db(query)
        all_reports=[]
        for row in results :
            report=cls(row)
            all_reports.append(report)   
        return all_reports 
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["message"])<8:
            is_valid = False
            flash("Message  is too short","message")
        return is_valid