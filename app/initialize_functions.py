from flask import Flask
from flasgger import Swagger
from app.db.db import db
from app.modules.iotgiroscopio.route import iotgiroscopio_bp
from app.modules.iotinsert.route import iotinsert_bp
from app.modules.main.route import main_bp

from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Initialize CORS first to allow cross-origin requests
    initialize_cors(app)
    
    # Initialize other components
    initialize_route(app)
    initialize_db(app)
    initialize_swagger(app)

    return app


def initialize_cors(app: Flask):
    """Initialize CORS configuration for Docker and localhost frontend servers"""
    # Get CORS origins from config if available, otherwise use defaults
    cors_origins = getattr(app.config, 'CORS_ORIGINS', [
        "http://localhost:3000",      # Common React dev server
        "http://localhost:8080",      # Common Vue.js dev server
        "http://localhost:5000",      # Flask dev server
        "http://localhost:5173",      # Vite dev server
        "http://localhost:4200",      # Angular dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:5050",
        "http://127.0.0.1:5500",
        "file://",                    # For local HTML files
        "null"                        # For file:// protocol
    ])
    
    CORS(app, 
         origins=cors_origins,
         allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True)


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(iotgiroscopio_bp, url_prefix='/api/v1/iotgiroscopio')
        app.register_blueprint(iotinsert_bp, url_prefix='/api/v1/iotinsert')
        app.register_blueprint(main_bp, url_prefix='/api/v1/main')

def initialize_db(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()

def initialize_swagger(app: Flask):
    with app.app_context():
        Swagger(app)
