# This routes

from flask import request, jsonify
from app import app, db
from models import User, ROLES


@app.route("/")
def index():
    return jsonify({"status": 200, "message": "Hello!, This API"}), 200


@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_list = [
            {"id": user.id, "username": user.username, "role": user.role}
            for user in users
        ]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/register", methods=["POST"])
def register():
    try:
        # GET Json
        data = request.get_json()

        if data["role"] not in ROLES:
            raise ValueError(f"Invalid role. Role must be one of {ROLES}.")

        new_user = User(username=data["username"], role=data["role"])
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": 201, "message": "User registered successfully!"}), 201

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        user = User.query.filter_by(username=data["username"]).first()

        if user and user.check_password(data["password"]):
            return (
                jsonify(
                    {"status": 200, "message": "Login successful!", "role": user.role}
                ),
                200,
            )
        else:
            return jsonify({"status": 401, "message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
