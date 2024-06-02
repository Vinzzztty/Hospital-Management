from dotenv import dotenv_values
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    config = dotenv_values(".env")
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "instance/hospital.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(
        config.get("PORT", 5000)
    )  # Ensure PORT is an integer, default to 5000 if not set
