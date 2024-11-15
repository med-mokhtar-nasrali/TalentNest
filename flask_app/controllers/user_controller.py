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
        session["user_id"] = user_id
        print (request.form["account_type"])
        if request.form["account_type"]=='1':
            print (request.form["account_type"])
        if request.form["account_type"]=='1':
            return redirect('/freelancer_form')
        if request.form["account_type"]=='0':
            return redirect('/recruiter_form')
    else:
        return redirect("/registration")
    
#Display Route For the login
@app.route("/login")
def login_page():
    if "user_id"  in session:
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
    return redirect("/login")


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


#Action Route for the freelancer profile form 


@app.route('/add_info/freelancer',methods=["post"])
def add_info():
    data = {
        **request.form,
        'user_id':session['user_id']
    }
    freelancer_id=Freelancer.add_freelancer_info(data)
    session['freelancer_id']=freelancer_id
    return redirect('/home')


#Action Route for the recruiter profile form 

@app.route('/add_info',methods=["post"])
def add_info_recruiter():
    data = {
        **request.form,
        'user_id':session['user_id']
    }
    recruiter_id=Recruiter.add_recruiter_info(data)
    session['recruiter_id']= recruiter_id
    return redirect('/home')
