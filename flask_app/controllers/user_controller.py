from flask_app import app
from flask_app.models.user_model import User
from flask import render_template,session,redirect,flash,request
from flask_bcrypt import Bcrypt
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
        return redirect("/home")
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
        print("this is before the flash")
        flash("Invalid Email/Password","login")
        print("this is after the flash")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password,request.form["password"]):
        flash("Invalid Email/Password","login")
        return redirect("/login")
    session["user_id"] = user.id
    return redirect("/home")

#Action Route to logout
@app.route("/logout",methods = ["POST"])
def logout():
    session.clear()
    return redirect("/")
