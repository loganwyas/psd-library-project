"""
This file creates a Flask app
"""
from flask import Flask, Response, request
import os
from flask_cors import CORS, cross_origin

# Creates the Flask app and configures it based on the correct environment
app = Flask(__name__)

# Configures the CORS policy to work with our React app
CLIENT_URLS = ["http://localhost:3001", "http://127.0.0.1:3001"]
cors = CORS(app, resources={r"*": {"origins": CLIENT_URLS}})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    print()