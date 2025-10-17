from flask import Flask
from app.config.config import get_config_by_name
from app.initialize_functions import initialize_route, initialize_db, initialize_swagger, initialize_cors

def create_app(config=None) -> Flask:
    """
    Create a Flask application.

    Args:
        config: The configuration object to use.

    Returns:
        A Flask application instance.
    """
    app = Flask(__name__)
    if config:
        app.config.from_object(get_config_by_name(config))

    # Initialize CORS first to handle preflight requests
    initialize_cors(app)

    # Initialize extensions
    initialize_db(app)

    # Register blueprints
    initialize_route(app)

    # Initialize Swagger
    initialize_swagger(app)

    return app
