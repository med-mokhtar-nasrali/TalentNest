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
        print ("before the data")
        data = {
            **request.form,
            'recruiter_id':session['recruiter_id']
        }
        print ("after the data")
        job_id=Job.add_job(data)
        session['job_id']= job_id
        return redirect ('/job_offers')
    return redirect('/job_form')


# this is the display route to display job offers

@app.route('/job_offers')
def show_all_jobs():
    print('*'*30)
    all_jobs=Job.show_all_jobs()
    print(all_jobs)
    
    return render_template('job_offers.html',all_jobs=all_jobs)

#applying to a job route
@app.route('/apply/<int:job_id>',methods=["post"])
def apply(job_id):
    Job.apply({'job_id':job_id,'freelancer_id':session['freelancer_id']})
    return redirect('/job_offers')


#delete job route in admin page 
@app.route('/delete_job/<int:id>', methods=["post"])
def delete_job(id):
    Job.delete_job({'id':id})
    return redirect ('/admin')



@app.route("/job_offers/<category>")
def show_all_by_category(category):
    if "user_id" not in session:
        return redirect('/login')
    list_of_jobs = Job.show_all_by_category({"category":category})
    print(list_of_jobs)
    return render_template("job_by_category.html", list_of_jobs=list_of_jobs)

@app.route("/search",methods=["post"])
def search():
    s = request.form["search"]
    return redirect(f"/job_offers/{s}")










