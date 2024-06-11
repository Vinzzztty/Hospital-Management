from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

bcrypt = Bcrypt()
mongo = PyMongo()


def create_user(username, role, password):
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user_id = mongo.db.users.insert_one(
        {"username": username, "role": role, "password": hashed_password}
    ).inserted_id

    return mongo.db.users.find_one({"_id": user_id})
