from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
)
from models.User import User
from db.db import db
import requests as http_request

app = Blueprint("user", "user", url_prefix="/api/users")


@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user_id": user.id}), 200


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if email is None or password is None:
        print("Email and password is required")
        print(email, password)
        return render_template("error.html", message="Bad email or password")

    token_data = http_request.post(
        "http://localhost:5000/api/users/token",
        json={"email": email, "password": password},
    )
    if token_data.status_code != 200:
        print("status code: " + str(token_data.status_code))
        return render_template("error.html", message="Something went wrong")
    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()["token"])
    return response


@app.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify({"users": [user.serialize() for user in users]}), 200


@app.route("/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify({"user": user.serialize()}), 200


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", None)
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    return render_template("login.html"), 201


@app.route("/", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"], password=data["password"])

    db.session.add(user)
    db.session.commit()
    return jsonify({"new_user": user.serialize()}), 201


@app.route("/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)

    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]

    db.session.commit()
    return jsonify({"updated_user": user.serialize()}), 200


@app.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"deleted_user": user.serialize()}), 200
