from flask_app.config.myconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models.user_model import User
from flask_app.models import recruiter_model
from flask_app.models import freelancer_model


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
        self.applied_freelancers=Job.get_applied_freelancers({'job_id':self.id})
    

    @classmethod
    def get_jobs_by_rectruter_id(cls,data):
        query="""  select * from recruiters
                    join jobs on jobs.recruiter_id= recruiters.id
                    join applications on jobs.id=applications.job_id 
                    join freelancers on applications.freelancer_id= freelancers.id
                    join users on freelancers.user_id=users.id
                    left join reviews on freelancers.user_id=reviews.freelancer_id
                    where jobs.recruiter_id=%(recruiter_id)s ;
                    """
        results=connectToMySQL(DB).query_db(query,data)
        # recruiter= recruiter_model.Recruiter(results[0])
        # job_list=[]
        # freelancers=[]
        # applications_list=[]
        # for row in results:
        #     job_data={
        #         **row,
        #         "id": row["jobs.id"],
        #         "created_at": row["jobs.created_at"],
        #         "updated_at": row["jobs.updated_at"]
        #     }
        #     job_list.append(cls(job_data))

        #     applications_list.append(row["recruiter_id"])

        # print (applications_list)
        return results
    @classmethod
    def deny_app(cls,data):
        query=  """ 
                update applications set status='Denied' where applications.job_id=%(job_id)s and applications.freelancer_id=%(freelancer_id)s ;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        return result
    

    @classmethod
    def get_applied_freelancers(cls,data):
        query="select * from applications where job_id=%(job_id)s ; "
        results=connectToMySQL(DB).query_db(query,data)
        all_freelancers_id=[] 
        for row in results :
            all_freelancers_id.append(row["freelancer_id"])
        return all_freelancers_id    


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
        return all_jobs 

    # deleting a job 
    @classmethod
    def delete_job(cls,data):
        query=  """ 
                DELETE FROM jobs WHERE jobs.id=%(id)s;
                """
        result = connectToMySQL( DB ).query_db(query,data)
        return result 


    #applying on a job offer 
    @classmethod
    def apply(cls,data):
        query=" insert into applications (job_id, freelancer_id, status) values(%(job_id)s,%(freelancer_id)s,'Pending') ;"
        result = connectToMySQL( DB ).query_db(query,data)
        return result

    @classmethod
    def show_all_by_category(cls,data):
        query="SELECT * FROM jobs WHERE category = %(category)s;"
        results=connectToMySQL( DB ).query_db(query,data)
        print(results)
        if results != False :
            all_jobs_by_category=[]
            for row in results:
                job=cls(row)
                all_jobs_by_category.append(job)
            return all_jobs_by_category
        else:
            return False


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data["title"])<3:
            is_valid = False
            flash("title is too short","title")

        if len(data["required_tech"])<1:
            is_valid = False
            flash("Required Tech can not be empty","required_tech ")

        x=int(data["budget"])
        if type(x) !=int:
            is_valid = False
            flash("Budget can not be empty","budget")

        if len(data["deadline"])<3:
            is_valid = False
            flash("Deadline can not be empty","deadline")
        if len(data["description"])<3:
            is_valid = False
            flash("description can not be empty","description")
                

        return is_valid    
