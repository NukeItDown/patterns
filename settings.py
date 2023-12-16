from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

class FlaskConfig:
    DEBUG = False

    JWT_HEADER_TYPE = ""
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = "sdgoinwerkiljbnwerfspuionbeo"

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/patterns'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(FlaskConfig)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)