from flask import Flask, send_from_directory
from flask_migrate import Migrate
from models import User
from routes import api_routes
from db_util import db
from populate_db import populate_db
from rate_limiter import limiter
import os
import logging

from flask_swagger_ui import get_swaggerui_blueprint


path_to_file = "users.json"
LOG_FILE = "app.log"

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

API_URL = "/static/openapi.yaml"
SWAGGER_URL = "/api/docs"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)


def config_app():
    # Initialize flask app with db, routes, rate-limits and migration configurations
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.create_all()  # Creates table on first startup if table not exists
        if not User.query.first():
            populate_db(path_to_file)

    Migrate(app, db)

    app.register_blueprint(api_routes)
    app.register_blueprint(swagger_blueprint)

    @app.route("/static/<path:filename>")
    def serve_openapi_spec(filename):
        return send_from_directory("static", filename)

    @app.route("/")
    def home():
        return "Welcome to Flask API!"

    @app.route("/health_check")
    def health_check():
        return {"message": "Health check successful"}

    return app


if __name__ == "__main__":
    flask_app = config_app()
    flask_app.run(host="0.0.0.0")
