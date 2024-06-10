from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import get_port, get_mongodb_uri
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app=app)

app.config["MONGO_URI"] = get_mongodb_uri()
mongo = PyMongo(app=app)

# # Initialize the MongoDB connection
# init_db(app)


@app.route("/")
def index():
    return "Welcome to the Flask-MongoDB app!"


@app.route("/users", methods=["GET"])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        result.append(
            {
                "_id": str(user["_id"]),
                "username": user["username"],
                "role": user["role"],
            }
        )
    return jsonify(result)


@app.route("/auth/register", methods=["POST"])
def add_user():
    username = request.json["username"]
    role = request.json["role"]
    password = request.json["password"]

    # Hashing password
    hash_password = bcrypt.generate_password_hash(password=password).decode("utf-8")

    user_id = mongo.db.users.insert_one(
        {"username": username, "role": role, "password": hash_password}
    ).inserted_id
    new_user = mongo.db.users.find_one({"_id": user_id})
    result = {
        "_id": str(new_user["_id"]),
        "username": new_user["username"],
        "role": new_user["role"],
        "password": new_user["password"],
    }
    return jsonify(result)


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Handling missing email and password not match
    if not username or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = mongo.db.users.find_one({"username": username})

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"message": f"Login successful, {user['role']}"})


if __name__ == "__main__":
    port = get_port()
    app.run(debug=True, port=port)
