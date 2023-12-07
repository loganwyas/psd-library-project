# Creates a Flask API and connects to the database

import json
from flask import Flask, Response, request
import os
from flask_cors import CORS, cross_origin
from database import Database

app = Flask(__name__)
CLIENT_URLS = ["http://localhost:3001", "http://127.0.0.1:3001"]
cors = CORS(app, resources={r"*": {"origins": CLIENT_URLS}})

# Attempt to login using account information
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
            "name": user[4],
            "profilePic": user[5]
        }
        status_code = 200
    return Response(
        json.dumps(data),
        mimetype="application/json",
        status=status_code,
    )

# Create an account
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
            "name": user[4],
            "profilePic": user[5]
        }
        status_code = 200
    return Response(
        json.dumps(data) if data else None,
        mimetype="application/json",
        status=status_code,
    )
    
# Edit profile information
@app.route("/profile", methods=["POST"])
@cross_origin()
def profile():
    user_info = request.get_json()
    db = Database()
    data = db.change_user_info(user_info["username"], user_info["password"], user_info["name"], user_info["profilePic"])
    status_code = 404
    if data:
        status_code = 200
    return Response(
        json.dumps(data) if data else None,
        mimetype="application/json",
        status=status_code,
    )

# Get catalog items based on search query
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
    
    data = db.get_catalog(searchValue)
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )
   
# Get library information based on the librarian 
@app.route("/library", methods=["GET"])
@cross_origin()
def library():
    db = Database()
    data = None
    user = None
    for arg, value in request.args.items():
        if arg == "user":
            user = value
    if user:
        data = db.get_library_from_user(user)
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )

# Get a list of all libraries
@app.route("/libraries", methods=["GET"])
@cross_origin()
def libraries():
    db = Database()
    data = db.get_libraries()
    return Response(
        json.dumps(data) if data else None,
        mimetype="application/json",
        status=(200 if data else 404),
    )
    
# Add an item to the library
@app.route("/add_library_item", methods=["POST"])
@cross_origin()
def add_library_item():
    catalog_item = request.get_json()
    db = Database()
    data = None
    library = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
    if library:
        data = db.add_library_item_count(library, catalog_item["id"], catalog_item["count"])
        
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )

# Edit a catalog item within a library
@app.route("/edit_library_item", methods=["POST"])
@cross_origin()
def edit_library_item():
    catalog_item = request.get_json()
    db = Database()
    data = None
    library = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
    if library:
        data = db.set_library_item_count(library, catalog_item["id"], catalog_item["count"])
        
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )

# Remove an item from a library
@app.route("/remove_library_item", methods=["POST"])
@cross_origin()
def remove_library_item():
    catalog_item = request.get_json()
    db = Database()
    success = False
    library = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
    if library:
        success = db.remove_library_item(library, catalog_item["id"])
        
    return Response(
        json.dumps(catalog_item) if success else None,
        mimetype="application/json",
        status=(200 if success else 404),
    )
    
# Get all items not in a specific library
@app.route("/unadded_library_items", methods=["GET"])
@cross_origin()
def unadded_library_items():
    db = Database()
    data = None
    library = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
    if library:
        data = db.get_unadded_library_items(library)
        
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )
    
# Checkout an item from the library
@app.route("/checkout_item", methods=["POST"])
@cross_origin()
def checkout_item():
    db = Database()
    success = None
    library = None
    user = None
    item = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
        elif arg == "user":
            user = value
        elif arg == "item":
            item = value
            
    if library and user and item:
        success = db.checkout_item(user, library, item)
        
    return Response(
        json.dumps([library, user, item]) if success else None,
        mimetype="application/json",
        status=(200 if success else 404),
    )
    
# Return an item to the library
@app.route("/return_item", methods=["POST"])
@cross_origin()
def return_item():
    db = Database()
    success = None
    library = None
    user = None
    item = None
    for arg, value in request.args.items():
        if arg == "library":
            library = value
        elif arg == "user":
            user = value
        elif arg == "item":
            item = value
            
    if library and user and item:
        success = db.return_item(user, library, item)
        
    return Response(
        json.dumps([library, user, item]) if success else None,
        mimetype="application/json",
        status=(200 if success else 404),
    )
    
# Get all user items
@app.route("/get_user_items", methods=["GET"])
@cross_origin()
def get_user_items():
    db = Database()
    data = None
    user = None
    for arg, value in request.args.items():
        if arg == "user":
            user = value
    if user:
        data = db.get_user_items(user)
        
    return Response(
        json.dumps(data) if data != None else None,
        mimetype="application/json",
        status=(200 if data != None else 404),
    )