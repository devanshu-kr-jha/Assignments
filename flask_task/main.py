from flask import Flask
from flask_migrate import Migrate
from models import User
from routes import api_routes
from db_util import db
from populate_db import populate_db
from rate_limiter import limiter

path_to_file = "users.json"


def config_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:password@localhost:5432/testDB2"
    )

    db.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.reflect()
        db.create_all()

        if not User.query.first():
            populate_db(path_to_file)

    Migrate(app, db)

    app.register_blueprint(api_routes)

    @app.route("/")
    def home():
        return "Welcome to Flask API!"

    @app.route("/health_check")
    def health_check():
        return {"message": "Health check successful"}

    return app


if __name__ == "__main__":
    flask_app = config_app()
    flask_app.run(debug=True)
