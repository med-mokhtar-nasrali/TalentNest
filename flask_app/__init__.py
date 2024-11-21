from flask import Flask
import stripe  # type: ignore
app = Flask(__name__)
app.secret_key = "put your secret key here"
DB = "talentnest_db"

STRIPE_PUBLIC_KEY = "pk_test_51QNW5hH7JyKzDcbartTtRzJe3WctaHLBwBEHfO1v3souBDeXpqhGZfdTUhT7Vf57Rjw83HQaNbWgxWM3berZKmmf00FPSu20Oz"
STRIPE_SECRET_KEY = "sk_test_51QNW5hH7JyKzDcbaBnXqNBheoh9oHmW0w0F8nixBoJzLxhA3qa7EE2dzss4H5zDbc6GCxtGVnoj8DvRYWzeWjJIQ0090n9y0vU"
stripe.api_key = STRIPE_SECRET_KEY