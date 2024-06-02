# This models

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

# Define the list of roles
ROLES = [
    "staff_ruangan",
    "staff_gudang",
    "atasan_langsung",
    "verifikasi",
    "pejabat_keuangan",
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates("role")
    def validate_role(self, key, role):
        if role not in ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {ROLES}.")
        return role

    def __repr__(self):
        return f"<User {self.username}>"
