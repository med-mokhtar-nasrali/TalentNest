from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.freelancer_model import Freelancer
from flask import render_template,session,redirect,flash,request

#Display Route for the edit page
@app.route('/freelancer/edit/<int:id>')
def edit(id):
    if "user_id"not in session:
        return redirect('/login')
    freelancer = Freelancer.get_by_id({"id":id})
    return render_template("edit_profile_freelancer.html",freelancer = freelancer)
    


#Action Route for the edit page
@app.route("/freelancer/update/<int:id>",methods=["POST"])
def update(id):
    if Freelancer.validate(request.form):
        data = {
            **request.form,
            "id":id
        }
        Freelancer.update(data)
        return redirect("/home")
    return redirect(f'/freelancer/edit/{id}')


#Display Route for the freelancer Profile
@app.route("/freelancer/profile")
def freelancer_profile():
    if "user_id"not in session:
        return redirect('/login')
    freelancer = Freelancer.get_all_freelancers_profile({"user_id":session["user_id"]})
    logged_user = User.get_user_by_id({"id":session["user_id"]})
    print(logged_user)
    print(freelancer)
    return render_template("freelancer_profile.html",user=logged_user,freelancer=freelancer)