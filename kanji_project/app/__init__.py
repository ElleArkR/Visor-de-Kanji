from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Database initialization
    from . import db
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.api_bp) # Register the API blueprint
    app.register_blueprint(routes.main_bp) # Register the main page blueprint

    return app
