from flask import Blueprint, request, jsonify
from bson import ObjectId
from models import mongo

sub_bagian_bp = Blueprint("sub_bagian", __name__, url_prefix="/sub_bagian")


# POST route to create a new sub_bag item (ajukan)
@sub_bagian_bp.route("/ajukan", methods=["POST"])
def ajukan():
    data = request.get_json()
    id_pengusulan_barang = data.get("id_pengusulan_barang")

    if not id_pengusulan_barang:
        return jsonify({"message": "Missing required fields"}), 400

    # Fetch the pengusulan_barang document
    pengusulan_barang = mongo.db.pengusulan_barang.find_one(
        {"_id": ObjectId(id_pengusulan_barang)}
    )

    if not pengusulan_barang:
        return jsonify({"message": "Referenced pengusulan_barang not found"}), 404

    # Extract details from the referenced document
    tanggal_pengusulan = pengusulan_barang.get("tanggal_pengusulan")
    tanggal_penerimaan = pengusulan_barang.get("tanggal_penerimaan")
    nama_barang = pengusulan_barang.get("nama_barang")
    volume = pengusulan_barang.get("volume")
    merek = pengusulan_barang.get("merek")

    sub_bag_id = mongo.db.sub_bag.insert_one(
        {
            "id_pengusulan_barang": id_pengusulan_barang,
            "tanggal_pengusulan": tanggal_pengusulan,
            "tanggal_penerimaan": tanggal_penerimaan,
            "nama_barang": nama_barang,
            "volume": volume,
            "merek": merek,
            "jumlah_diterima": 0,  # Default value
            "is_verif": False,  # Set is_verif to False by default
        }
    ).inserted_id

    new_sub_bag = mongo.db.sub_bag.find_one({"_id": sub_bag_id})
    new_sub_bag["_id"] = str(new_sub_bag["_id"])  # Convert ObjectId to string
    new_sub_bag["id_pengusulan_barang"] = str(
        new_sub_bag["id_pengusulan_barang"]
    )  # Ensure reference ID is also a string

    return jsonify(new_sub_bag), 201


# GET route to retrieve all sub_bag items
@sub_bagian_bp.route("/ajukan", methods=["GET"])
def get_all_ajukan():
    sub_bag_items = list(mongo.db.sub_bag.find())

    # Convert ObjectId to string for JSON serialization
    for item in sub_bag_items:
        item["_id"] = str(item["_id"])
        item["id_pengusulan_barang"] = str(item["id_pengusulan_barang"])

    return jsonify({"sub_bag": sub_bag_items}), 200


# GET route to retrieve a specific sub_bag item by ID
@sub_bagian_bp.route("/ajukan/<ajukan_id>", methods=["GET"])
def get_ajukan_detail(ajukan_id):
    sub_bag_item = mongo.db.sub_bag.find_one({"_id": ObjectId(ajukan_id)})

    if not sub_bag_item:
        return jsonify({"message": "Ajukan not found"}), 404

    sub_bag_item["_id"] = str(sub_bag_item["_id"])  # Convert ObjectId to string
    sub_bag_item["id_pengusulan_barang"] = str(sub_bag_item["id_pengusulan_barang"])

    return jsonify(sub_bag_item), 200


# POST route for verification
@sub_bagian_bp.route("/verifikasi", methods=["POST"])
def verifikasi():
    data = request.get_json()
    ajukan_id = data.get("id_ajukan")
    jumlah_diterima = data.get("jumlah_diterima")

    if not ajukan_id or jumlah_diterima is None:
        return jsonify({"message": "Missing required fields"}), 400

    ajukan = mongo.db.sub_bag.find_one({"_id": ObjectId(ajukan_id)})
    if not ajukan:
        return jsonify({"message": "Invalid id_ajukan"}), 400

    volume = ajukan["volume"]

    if jumlah_diterima > volume:
        return (
            jsonify({"message": "Jumlah diterima cannot be greater than volume"}),
            400,
        )

    is_verif = jumlah_diterima == volume

    result = mongo.db.sub_bag.update_one(
        {"_id": ObjectId(ajukan_id)},
        {"$set": {"jumlah_diterima": jumlah_diterima, "is_verif": is_verif}},
    )

    if result.modified_count == 1:
        return jsonify({"message": "Verification completed successfully"})
    else:
        return jsonify({"message": "Verification failed"}), 500


@sub_bagian_bp.route("/verifikasi_true", methods=["GET"])
def get_verified_ajukan():
    verified_items = list(mongo.db.sub_bag.find({"is_verif": True}))
    for item in verified_items:
        item["_id"] = str(item["_id"])
    return jsonify({"verified_sub_bag": verified_items})


@sub_bagian_bp.route("/verifikasi_false", methods=["GET"])
def get_unverified_ajukan():
    unverified_items = list(mongo.db.sub_bag.find({"is_verif": False}))
    for item in unverified_items:
        item["_id"] = str(item["_id"])
    return jsonify({"unverified_sub_bag": unverified_items})


################################################################################

# # GET route to retrieve sub_bag_verifikasi items
# @sub_bagian_bp.route("/sub_bag_verifikasi", methods=["GET"])
# def get_sub_bag_verifikasi():
#     sub_bag_verifikasi_items = list(
#         mongo.db.pengusulan_barang.find({}, {"tanggal": 1, "ruangan": 1})
#     )

#     # Convert ObjectId to string for JSON serialization
#     for item in sub_bag_verifikasi_items:
#         item["_id"] = str(item["_id"])

#     return jsonify({"sub_bag_verifikasi": sub_bag_verifikasi_items})


# # # GET route to retrieve sub_bag_verifikasi items by ruangan
# @sub_bagian_bp.route("/sub_bag_verifikasi/<ruangan>", methods=["GET"])
# def get_sub_bag_verifikasi_by_ruangan(ruangan):
#     sub_bag_verifikasi_items = list(
#         mongo.db.pengusulan_barang.find(
#             {"ruangan": ruangan},
#             {"tanggal": 1, "ruangan": 1, "nama_barang": 1, "volume": 1},
#         )
#     )

#     # Convert ObjectId to string for JSON serialization
#     for item in sub_bag_verifikasi_items:
#         item["_id"] = str(item["_id"])

#     return jsonify({"sub_bag_verifikasi": sub_bag_verifikasi_items})


# # GET route to retrieve all verifikasi items
# @sub_bagian_bp.route("/verifikasi", methods=["GET"])
# def get_all_verifikasi():
#     verifikasi_items = list(
#         mongo.db.verifikasi.find(
#             {}, {"id_pengusulan_barang": 1, "volume": 1, "is_verif_sub_bag": 1}
#         )
#     )

#     # Convert ObjectId to string for JSON serialization
#     for item in verifikasi_items:
#         item["_id"] = str(item["_id"])
#         item["id_pengusulan_barang"] = str(item["id_pengusulan_barang"])

#     return jsonify({"verifikasi": verifikasi_items})


# # GET route to retrieve verifikasi items by ruangan (through pengusulan_barang)
# @sub_bagian_bp.route("/verifikasi/ruangan/<ruangan>", methods=["GET"])
# def get_verifikasi_by_ruangan(ruangan):
#     pengusulan_items = list(
#         mongo.db.pengusulan_barang.find({"ruangan": ruangan}, {"_id": 1})
#     )

#     # Extract the IDs of the relevant pengusulan_barang
#     pengusulan_ids = [item["_id"] for item in pengusulan_items]

#     verifikasi_items = list(
#         mongo.db.verifikasi.find(
#             {"id_pengusulan_barang": {"$in": pengusulan_ids}},
#             {"id_pengusulan_barang": 1, "volume": 1, "is_verif_sub_bag": 1},
#         )
#     )

#     # Convert ObjectId to string for JSON serialization
#     for item in verifikasi_items:
#         item["_id"] = str(item["_id"])
#         item["id_pengusulan_barang"] = str(item["id_pengusulan_barang"])

#     return jsonify({"verifikasi": verifikasi_items})


# # POST route to add a verifikasi item
# @sub_bagian_bp.route("/verifikasi", methods=["POST"])
# def add_verifikasi():
#     data = request.get_json()
#     id_pengusulan_barang = data.get("id_pengusulan_barang")
#     volume = data.get("volume")

#     if not id_pengusulan_barang or not volume:
#         return (
#             jsonify(
#                 {
#                     "message": "id_pengusulan_barang, nama_barang, and volume are required"
#                 }
#             ),
#             400,
#         )

#     verifikasi_id = mongo.db.verifikasi.insert_one(
#         {
#             "id_pengusulan_barang": ObjectId(id_pengusulan_barang),
#             "nama_barang": nama_barang,
#             "volume": volume,
#             "is_verif_sub_bag": 0,
#         }
#     ).inserted_id

#     new_verifikasi = mongo.db.verifikasi.find_one({"_id": verifikasi_id})

#     result = {
#         "_id": str(new_verifikasi["_id"]),
#         "id_pengusulan_barang": str(new_verifikasi["id_pengusulan_barang"]),
#         "nama_barang": new_verifikasi["nama_barang"],
#         "volume": new_verifikasi["volume"],
#         "is_verif_sub_bag": new_verifikasi["is_verif_sub_bag"],
#     }

#     return jsonify(result)


# # PUT route to update the is_verif_sub_bag field
# @sub_bagian_bp.route("/verifikasi/<id>", methods=["PUT"])
# def update_verifikasi(id):
#     data = request.get_json()
#     is_verif_sub_bag = data.get("is_verif_sub_bag")

#     if is_verif_sub_bag is None:
#         return jsonify({"message": "is_verif_sub_bag is required"}), 400

#     result = mongo.db.verifikasi.update_one(
#         {"_id": ObjectId(id)}, {"$set": {"is_verif_sub_bag": is_verif_sub_bag}}
#     )

#     if result.matched_count == 0:
#         return jsonify({"message": "Verifikasi not found"}), 404

#     updated_verifikasi = mongo.db.verifikasi.find_one({"_id": ObjectId(id)})

#     result = {
#         "_id": str(updated_verifikasi["_id"]),
#         "id_pengusulan_barang": str(updated_verifikasi["id_pengusulan_barang"]),
#         "volume": updated_verifikasi["volume"],
#         "is_verif_sub_bag": updated_verifikasi["is_verif_sub_bag"],
#     }

#     return jsonify(result)
