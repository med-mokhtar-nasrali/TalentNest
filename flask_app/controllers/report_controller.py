from flask_app import app
from flask_app.models.report_model import Report
from flask import render_template,session,redirect,flash,request



@app.route("/user/report/<int:id>")
def report_display(id):
    if "user_id"not in session:
        return redirect('/login')
    return render_template("report_form.html" , id=id)


@app.route("/report/user",methods=["POST"])
def report_send():
    if Report.validate(request.form):
        data = {
            **request.form,
            'sender_id':session['user_id']
        }
        Report.add_report(data)
        
        return redirect('/home')
    return redirect("/user/report")