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