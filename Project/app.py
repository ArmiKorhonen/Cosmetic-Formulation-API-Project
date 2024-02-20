from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, abort
from api import api_bp
from models import db  # Import the SQLAlchemy instance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cosme-api-project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

# Initialize the database with the app
db.init_app(app)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
