from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Configure application
app = Flask(__name__)

import homeaway.views
from homeaway.models import db

# Set the sessions' secret key to some random bytes.
app.secret_key = environ.get('SECRET_KEY')

# DATABASE SETUP START
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    # connect to development database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homeaway'
else:
    app.debug = False
    # connect to production database
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize db
db.init_app(app)

# create database tables from models
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()
