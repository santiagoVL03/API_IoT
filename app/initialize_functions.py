from app.modules.iotgiroscopio.route import iotgiroscopio_bp
from app.modules.iotinsert.route import iotinsert_bp
from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp
from app.db.db import db


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
        swagger = Swagger(app)
        return swagger