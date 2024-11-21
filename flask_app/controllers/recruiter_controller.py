from flask_app import app
from flask_app import STRIPE_PUBLIC_KEY,STRIPE_SECRET_KEY
from flask_app.models.recruiter_model import Recruiter
from flask import render_template,session,redirect,flash,request,jsonify
import stripe # type: ignore


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


@app.route('/payment', methods=['GET'])
def payment():
    return render_template('payment.html', public_key=STRIPE_PUBLIC_KEY)



@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Payment of 10%',
                    },
                    'unit_amount': 2000,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    
