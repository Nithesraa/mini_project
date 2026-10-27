import os
from flask import Flask
from config import SECRET_KEY, DEBUG, MAX_CONTENT_LENGTH
from routes.main_routes import main_bp
from routes.api_routes import api_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
