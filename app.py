from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config  # Import Config from config.py


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db=db)

# Routes
from routes import *


if __name__ == "__main__":
    app.run(debug=True, port=Config.PORT)
