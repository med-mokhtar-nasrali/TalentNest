from flask_app import app
from flask_app.models.report_model import Report
from flask import render_template,session,redirect,flash,request



@app.route("/user/report")
def report_display():
    if "user_id"not in session:
        return redirect('/login')
    return render_template("report_form.html")


# @app.route("/report/user",methods=["POST"])
# def report_send():
#     if Report.validate(request.form):
#         data = {
#             **request.form,
#             'user_id':session['user_id']
#         }
#         report_id=Report.add_report(data)
#         session['reporter_id']=report_id
#         return redirect('/home')