from flask import Blueprint, request, jsonify, render_template
from models import User, Todo
from db.db import db

app = Blueprint("todo", "todo", url_prefix="/api/todo")


@app.route("/<int:id>", methods=["GET"])
def get_user_todos(id):
    todos = Todo.query.filter(Todo.user_id == id).all()
    return jsonify({"todos": [todo.serialize() for todo in todos]}), 200


@app.route("/all", methods=["GET"])
def get_todo():
    todos = Todo.query.all()
    return jsonify({"todos": [todo.serialize() for todo in todos]}), 200


@app.route("/<int:id>", methods=["POST"])
def create_todo(id):
    data = request.json
    user = User.query.get(id)

    todo = Todo(title=data["title"], content=data["content"], check=False, user_id=id)

    db.session.add(todo)
    db.session.commit()
    return jsonify({"new_todo": todo.serialize(), "user": user.serialize()}), 201


@app.route("/<int:id>", methods=["PUT"])
def update_todo(id):
    data = request.json
    todo = Todo.query.get(id)

    todo.title = data["title"]
    todo.content = data["content"]

    db.session.commit()
    return jsonify({"updated_todo": todo.serialize()}), 200


@app.route("/check/<int:id>", methods=["PUT"])
def check_todo(id):
    todo = Todo.query.get(id)

    todo.check = not todo.check

    db.session.commit()
    return jsonify({"todo": todo.serialize()}), 200


@app.route("/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo = Todo.query.get(id)

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"deleted_todo": todo.serialize()}), 200
