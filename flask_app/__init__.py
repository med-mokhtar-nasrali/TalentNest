from flask import Flask
app = Flask(__name__)
app.secret_key = "put your secret key here"
DB = "talentnest_db"