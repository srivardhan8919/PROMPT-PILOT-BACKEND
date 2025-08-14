from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)
    print(f"MongoDB URI: {app.config.get('MONGO_URI')}")
    if mongo.db is None:
        print("ERROR: PyMongo failed to connect. Check your MONGO_URI and MongoDB server.")
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    from app.routes.llm import llm_bp
    app.register_blueprint(llm_bp, url_prefix="/api/llm")
    from app.routes.health import health_bp
    app.register_blueprint(health_bp)

    return app
