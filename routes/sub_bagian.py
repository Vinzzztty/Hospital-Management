from flask import Blueprint, request, jsonify
from bson import ObjectId
from models import mongo

sub_bagian_bp = Blueprint("sub_bagian", __name__, url_prefix="/sub_bagian")


# GET route to retrieve sub_bag_verifikasi items
@sub_bagian_bp.route("/sub_bag_verifikasi", methods=["GET"])
def get_sub_bag_verifikasi():
    sub_bag_verifikasi_items = list(
        mongo.db.pengusulan_barang.find({}, {"tanggal": 1, "ruangan": 1})
    )

    # Convert ObjectId to string for JSON serialization
    for item in sub_bag_verifikasi_items:
        item["_id"] = str(item["_id"])

    return jsonify({"sub_bag_verifikasi": sub_bag_verifikasi_items})


# # GET route to retrieve sub_bag_verifikasi items by ruangan
@sub_bagian_bp.route("/sub_bag_verifikasi/<ruangan>", methods=["GET"])
def get_sub_bag_verifikasi_by_ruangan(ruangan):
    sub_bag_verifikasi_items = list(
        mongo.db.pengusulan_barang.find(
            {"ruangan": ruangan},
            {"tanggal": 1, "ruangan": 1, "nama_barang": 1, "volume": 1},
        )
    )

    # Convert ObjectId to string for JSON serialization
    for item in sub_bag_verifikasi_items:
        item["_id"] = str(item["_id"])

    return jsonify({"sub_bag_verifikasi": sub_bag_verifikasi_items})


# GET route to retrieve all verifikasi items
@sub_bagian_bp.route("/verifikasi", methods=["GET"])
def get_all_verifikasi():
    verifikasi_items = list(
        mongo.db.verifikasi.find(
            {}, {"id_pengusulan_barang": 1, "volume": 1, "is_verif_sub_bag": 1}
        )
    )

    # Convert ObjectId to string for JSON serialization
    for item in verifikasi_items:
        item["_id"] = str(item["_id"])
        item["id_pengusulan_barang"] = str(item["id_pengusulan_barang"])

    return jsonify({"verifikasi": verifikasi_items})


# GET route to retrieve verifikasi items by ruangan (through pengusulan_barang)
@sub_bagian_bp.route("/verifikasi/ruangan/<ruangan>", methods=["GET"])
def get_verifikasi_by_ruangan(ruangan):
    pengusulan_items = list(
        mongo.db.pengusulan_barang.find({"ruangan": ruangan}, {"_id": 1})
    )

    # Extract the IDs of the relevant pengusulan_barang
    pengusulan_ids = [item["_id"] for item in pengusulan_items]

    verifikasi_items = list(
        mongo.db.verifikasi.find(
            {"id_pengusulan_barang": {"$in": pengusulan_ids}},
            {"id_pengusulan_barang": 1, "volume": 1, "is_verif_sub_bag": 1},
        )
    )

    # Convert ObjectId to string for JSON serialization
    for item in verifikasi_items:
        item["_id"] = str(item["_id"])
        item["id_pengusulan_barang"] = str(item["id_pengusulan_barang"])

    return jsonify({"verifikasi": verifikasi_items})


# POST route to add a verifikasi item
@sub_bagian_bp.route("/verifikasi", methods=["POST"])
def add_verifikasi():
    data = request.get_json()
    id_pengusulan_barang = data.get("id_pengusulan_barang")
    nama_barang = data.get("nama_barang")
    volume = data.get("volume")

    if not id_pengusulan_barang or not nama_barang or not volume:
        return (
            jsonify(
                {
                    "message": "id_pengusulan_barang, nama_barang, and volume are required"
                }
            ),
            400,
        )

    verifikasi_id = mongo.db.verifikasi.insert_one(
        {
            "id_pengusulan_barang": ObjectId(id_pengusulan_barang),
            "nama_barang": nama_barang,
            "volume": volume,
            "is_verif_sub_bag": 0,
        }
    ).inserted_id

    new_verifikasi = mongo.db.verifikasi.find_one({"_id": verifikasi_id})

    result = {
        "_id": str(new_verifikasi["_id"]),
        "id_pengusulan_barang": str(new_verifikasi["id_pengusulan_barang"]),
        "nama_barang": new_verifikasi["nama_barang"],
        "volume": new_verifikasi["volume"],
        "is_verif_sub_bag": new_verifikasi["is_verif_sub_bag"],
    }

    return jsonify(result)


# PUT route to update the is_verif_sub_bag field
@sub_bagian_bp.route("/verifikasi/<id>", methods=["PUT"])
def update_verifikasi(id):
    data = request.get_json()
    is_verif_sub_bag = data.get("is_verif_sub_bag")

    if is_verif_sub_bag is None:
        return jsonify({"message": "is_verif_sub_bag is required"}), 400

    result = mongo.db.verifikasi.update_one(
        {"_id": ObjectId(id)}, {"$set": {"is_verif_sub_bag": is_verif_sub_bag}}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Verifikasi not found"}), 404

    updated_verifikasi = mongo.db.verifikasi.find_one({"_id": ObjectId(id)})

    result = {
        "_id": str(updated_verifikasi["_id"]),
        "id_pengusulan_barang": str(updated_verifikasi["id_pengusulan_barang"]),
        "volume": updated_verifikasi["volume"],
        "is_verif_sub_bag": updated_verifikasi["is_verif_sub_bag"],
    }

    return jsonify(result)
