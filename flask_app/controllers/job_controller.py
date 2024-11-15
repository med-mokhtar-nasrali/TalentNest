from flask_app import app
from flask_app.models.job_model import Job
from flask import render_template,session,redirect,request

#this is the display route for the job creation form 
@app.route('/job_form')
def job_create():
    if "user_id" not in session:
        return redirect('/login')
    return render_template('job_offer.html')




#this is the action route for validating the job data and adding it in the database then retuning to the home page

@app.route('/add_job',methods=["post"])
def add_job():
    if Job.validate(request.form):
        data = {
            **request.form,
            'recruiter_id':session['recruiter_id']
        }
        job_id=Job.add_job(data)
        session['job_id']= job_id
        return redirect ('/home')
    return redirect('/job_form')





