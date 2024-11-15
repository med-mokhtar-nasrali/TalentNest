from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.account_type = data["account_type"]
        self.profile_pic = data["profile_pic"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


#This is a query for the registration form to insert user data into the tables
    @classmethod
    def register(cls,data):
        query = """
                INSERT INTO users (first_name,last_name,email,password,account_type)
                VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(account_type)s)
                """
        return connectToMySQL( DB ).query_db(query,data)
    

    @classmethod
    def get_by_email(cls,data):
        query = """
                SELECT * FROM users WHERE email=%(email)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        if result:
            print(cls(result[0]))
            return cls(result[0])
        return False
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT id FROM users WHERE email=%(email)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        if result:
            return cls(result[0])
        return False

#this function will return 0 or 1 to know the type of the user account
    @classmethod
    def get_account_type(cls,data):
        query="select account_type from users where users.id=%(id)s;"
        result=connectToMySQL( DB ).query_db(query,data)
        return result





#this is the validation method for the registration 

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["first_name"])<2:
            flash("Last Name must at least 2 characters","first_name")
            is_valid = False
        if len(data["last_name"])<2:
            flash("Last Name must at least 2 characters","last_name")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email format is not valid","email")
            is_valid = False
        elif User.get_by_email({"email": data["email"]}):
            flash("Email is already taken!","email")
            is_valid = False
        if len(data["password"])<8:
            flash("Password must at least 8 characters","password")
            is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash("Passwords don't match","confirm_password")
            is_valid = False
        return is_valid