from flask_app import app
from flask_app.models.recruiter_model import Recruiter
from flask import render_template,session,redirect,flash,request

#Display Route for the edit page
@app.route('/recruiter/edit/<int:id>')
def edit_recruiter(id):
    if "user_id"not in session:
        return redirect('/login')
    recruiter = Recruiter.get_by_id({"id":id})
    return render_template("edit_profile_recruiter.html",recruiter = recruiter)


#Action Route for the edit page
@app.route("/recruiter/update/<int:id>",methods=["POST"])
def update_recruiter(id):
    if Recruiter.validate(request.form):
        data = {
            **request.form,
            "id":id
        }
        Recruiter.update(data)
        return redirect("/home")
    return redirect(f'/recruiter/edit/{id}')


#Display Route for the recruiter Profile
@app.route("/recruiter/profile")
def recruiter_profile():
    if "user_id"not in session:
        return redirect('/login')
    return render_template("recruiter_profile.html")


