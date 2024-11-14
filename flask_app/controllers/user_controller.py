from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.freelancer_model import Freelancer
from flask_app.models.recruiter_model import Recruiter
from flask import render_template,session,redirect,flash,request
from flask_bcrypt import Bcrypt # type: ignore
bcrypt = Bcrypt(app)


#Display Route For the landing page
@app.route("/")
def index():
    return render_template("home_before.html")

#Display Route For the registration page
@app.route("/registration")
def registration():
    return render_template("/registration_form.html")

#Action Route to validate user data and add it to DB
@app.route("/user/create",methods = ["POST"])
def register():
    if User.validate(request.form):
        pw = bcrypt.generate_password_hash(request.form["password"])
        data = {
            **request.form,
            "password":pw
        }
        user_id = User.register(data)
        print (user_id)
        session["user_id"] = user_id
        print (session["user_id"])
        if request.form["account_type"]==1:
            return redirect('/freelancer_form')
        else:
            return redirect('/recruiter_form')
        
    else:
        return redirect("/registration")
    
#Display Route For the login
@app.route("/login")
def login_page():
    if "user_id" in session:
        return redirect('/home')
    return render_template("/login_form.html")
    
#Action Route for the login
@app.route('/user/login',methods = ["POST"])
def login():
    user = User.get_by_email({"email":request.form["email"]})
    if not user :
        flash("Invalid Email/Password","login")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password,request.form["password"]):
        flash("Invalid Email/Password","login")
        return redirect("/login")
    session["email"] = user.email
    session["user_id"] = user.id
    return redirect("/home")

#Action Route to logout
@app.route("/logout",methods = ["POST"])
def logout():
    session.clear()
    return redirect("/")


#Display route for freelancer form

@app.route("/freelancer_form")
def register_freelancer():
    if "user_id" not in session:
        return redirect('/login')
    return render_template("more_freelancer_info.html")


#Display route for recruiter form

@app.route("/recruiter_form")
def register_recruiter():
    if "user_id" not in session:
        return redirect('/login')
    return render_template("more_recruiter_info.html")




@app.route('/add_info',methods=["post"])
def add_info():
    result=User.get_account_type(session['email'])
    if result==1 :
        freelancer_id=User.get_by_id(session['email'])
        data = {
            **request.form,
            'user_id':freelancer_id
        }
        Freelancer.add_freelancer_info(data)
    else: 
        recruiter_id=User.get_by_id(session['email'])
        data = {
            **request.form,
            'user_id':recruiter_id
        }
        Recruiter.add_recruiter_info(data)
    return redirect('/home')
