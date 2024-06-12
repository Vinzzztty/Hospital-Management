from flask import Flask, jsonify
from bson.objectid import ObjectId
from config import get_port, get_mongodb_uri
from models import bcrypt, mongo
from routes.auth import auth_bp
from routes.staffRuangan import staff_ruangan_bp
from routes.sub_bagian import sub_bagian_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

# Initialize database and bcrypt
app.config["MONGO_URI"] = get_mongodb_uri()
mongo.init_app(app)
bcrypt.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(staff_ruangan_bp)
app.register_blueprint(sub_bagian_bp)


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


if __name__ == "__main__":
    port = get_port()
    app.run(debug=True, port=port)
