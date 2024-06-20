from flask import Blueprint, jsonify
from bson.objectid import ObjectId
from models import mongo
from pymongo.errors import PyMongoError

transaksi_bp = Blueprint("api/transaksi", __name__, url_prefix="/api/transaksi")

# transaksi_bp = Blueprint("transaksi", __name__, url_prefix="/transaksi")


# @transaksi_bp.route("/", methods=["POST"])
# def save_and_get_transaksi():
#     try:
#         # Initialize the data to store in transaksi
#         all_transaksi = []

#         # Fetch data from MongoDB collections for each role
#         sub_bag_transaksi = list(mongo.db.sub_bag.find())
#         kepala_bagian_transaksi = list(mongo.db.kepala_bagian.find())
#         verifikasi_transaksi = list(mongo.db.verifikasi.find())

#         # Convert ObjectId to string for JSON serialization and prepare to save
#         for item in sub_bag_transaksi:
#             item["_id"] = str(item["_id"])
#             item["role"] = "sub_bag"
#             all_transaksi.append(item)
#         for item in kepala_bagian_transaksi:
#             item["_id"] = str(item["_id"])
#             item["role"] = "kepala_bagian"
#             all_transaksi.append(item)
#         for item in verifikasi_transaksi:
#             item["_id"] = str(item["_id"])
#             item["role"] = "verifikasi"
#             all_transaksi.append(item)

#         # Insert the data into the transaksi collection
#         insert_result = mongo.db.transaksi.insert_many(all_transaksi)

#         # Retrieve the inserted data to return
#         inserted_ids = insert_result.inserted_ids
#         stored_transaksi = list(mongo.db.transaksi.find({"_id": {"$in": inserted_ids}}))

#         # Convert ObjectId to string for JSON serialization
#         for item in stored_transaksi:
#             item["_id"] = str(item["_id"])

#         return jsonify(stored_transaksi), 201

#     except PyMongoError as e:
#         error_message = f"MongoDB error: {str(e)}"
#         return jsonify({"error": error_message}), 500


# @transaksi_bp.route("/", methods=["GET"])
# def get_all_transaksi():
#     all_transaksi = {
#         "sub_bag_transaksi": [],
#         "kepala_bagian_transaksi": [],
#         "verifikasi_transaksi": [],
#     }

#     try:
#         # Fetch data from MongoDB collections for each role
#         sub_bag_transaksi = list(mongo.db.sub_bag.find())
#         kepala_bagian_transaksi = list(mongo.db.kepala_bagian.find())
#         verifikasi_transaksi = list(mongo.db.verifikasi.find())

#         # Convert ObjectId to string for JSON serialization
#         for item in sub_bag_transaksi:
#             item["_id"] = str(item["_id"])
#         for item in kepala_bagian_transaksi:
#             item["_id"] = str(item["_id"])
#         for item in verifikasi_transaksi:
#             item["_id"] = str(item["_id"])

#         # Add fetched data to the response dictionary
#         all_transaksi["sub_bag_transaksi"] = sub_bag_transaksi
#         all_transaksi["kepala_bagian_transaksi"] = kepala_bagian_transaksi
#         all_transaksi["verifikasi_transaksi"] = verifikasi_transaksi

#         return jsonify(all_transaksi), 200

#     except PyMongoError as e:
#         error_message = f"MongoDB error: {str(e)}"
#         return jsonify({"error": error_message}), 500


@transaksi_bp.route("/", methods=["GET"])
def get_all_transaksi():
    all_transaksi = {
        "sub_bag_transaksi": [],
        "kepala_bagian_transaksi": [],
        "verifikasi_transaksi": [],
    }

    try:
        # Fetch data from MongoDB collections for each role
        sub_bag_transaksi = list(mongo.db.sub_bag.find())
        kepala_bagian_transaksi = list(mongo.db.kepala_bagian.find())
        verifikasi_transaksi = list(mongo.db.verifikasi.find())

        # Convert ObjectId to string for JSON serialization
        for item in sub_bag_transaksi:
            item["_id"] = str(item["_id"])
        for item in kepala_bagian_transaksi:
            item["_id"] = str(item["_id"])
        for item in verifikasi_transaksi:
            item["_id"] = str(item["_id"])

        # Add fetched data to the response dictionary
        all_transaksi["sub_bag_transaksi"] = sub_bag_transaksi
        all_transaksi["kepala_bagian_transaksi"] = kepala_bagian_transaksi
        all_transaksi["verifikasi_transaksi"] = verifikasi_transaksi

        return jsonify(all_transaksi), 200

    except PyMongoError as e:
        error_message = f"MongoDB error: {str(e)}"
        return jsonify({"error": error_message}), 500


@transaksi_bp.route("/decline", methods=["GET"])
def get_declined_transaksi():
    try:
        # Find transactions where is_verif is False in either kepala_bagian or verifikasi
        declined_items = []

        kepala_bagian_declined = list(mongo.db.kepala_bagian.find({"is_verif": False}))
        verifikasi_declined = list(mongo.db.verifikasi.find({"is_verif": False}))

        declined_items.extend(kepala_bagian_declined)
        declined_items.extend(verifikasi_declined)

        for item in declined_items:
            item["_id"] = str(item["_id"])
        return jsonify({"declined_transaksi": declined_items}), 200

    except PyMongoError as e:
        error_message = f"MongoDB error: {str(e)}"
        return jsonify({"error": error_message}), 500


@transaksi_bp.route("/success", methods=["GET"])
def get_successful_transaksi():
    try:
        # Find transactions where is_verif is True in verifikasi
        successful_items = list(mongo.db.verifikasi.find({"is_verif": True}))
        for item in successful_items:
            item["_id"] = str(item["_id"])
        return jsonify({"successful_transaksi": successful_items}), 200

    except PyMongoError as e:
        error_message = f"MongoDB error: {str(e)}"
        return jsonify({"error": error_message}), 500


@transaksi_bp.route("/on_process", methods=["GET"])
def get_on_process_transaksi():
    try:
        # Find transactions where is_verif is False in sub_bag
        on_process_items = list(mongo.db.sub_bag.find({"is_verif": False}))
        for item in on_process_items:
            item["_id"] = str(item["_id"])
        return jsonify({"on_process_transaksi": on_process_items}), 200

    except PyMongoError as e:
        error_message = f"MongoDB error: {str(e)}"
        return jsonify({"error": error_message}), 500
