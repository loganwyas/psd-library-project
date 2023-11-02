"""
This file creates a Flask app
"""
import json
from flask import Flask, Response, request
import os
from flask_cors import CORS, cross_origin
from database import Database

# Creates the Flask app and configures it based on the correct environment
app = Flask(__name__)

# Configures the CORS policy to work with our React app
CLIENT_URLS = ["http://localhost:3001", "http://127.0.0.1:3001"]
cors = CORS(app, resources={r"*": {"origins": CLIENT_URLS}})

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    user_info = request.get_json()
    db = Database()
    user = db.login(user_info["username"], user_info["password"])
    data = {}
    status_code = 404
    if user:
        data = {
            "id": user[3],
            "username": user[0],
            "password": user[1],
            "role": user[2],
        }
        status_code = 200
    return Response(
        json.dumps(data),
        mimetype="application/json",
        status=status_code,
    )
    
@app.route("/create_account", methods=["POST"])
@cross_origin()
def create_account():
    user_info = request.get_json()
    db = Database()
    user = db.add_user(user_info["username"], user_info["password"], user_info["role"])
    data = None
    status_code = 404
    if user:
        data = {
            "id": user[3],
            "username": user[0],
            "password": user[1],
            "role": user[2],
        }
        status_code = 200
    return Response(
        json.dumps(data) if data else None,
        mimetype="application/json",
        status=status_code,
    )
    
@app.route("/catalog", methods=["GET"])
@cross_origin()
def catalog():
    db = Database()
    data = None
    searchValue = ""
    for arg, value in request.args.items():
        if arg == "search":
            array = value.split(" ")
            for index, val in enumerate(array):
                if val != "":
                    searchValue += val
                    if index != len(array) - 1:
                        searchValue += " "
    
                    
    return Response(
        json.dumps(data) if data else None,
        mimetype="application/json",
        status=200,
    )  