from flask_app import app
from flask_app.controllers import user_controller,freelancer_controller,recruiter_controller,job_controller,report_controller


if __name__ == "__main__":
    app.run(debug=True)