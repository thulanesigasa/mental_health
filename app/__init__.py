from flask import Flask
from config import Config
from app.extensions import db, migrate, limiter

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Import models so Alembic can discover them
    from app import models

    # Register blueprints
    from app.views.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.views.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.views.modules import bp as modules_bp
    app.register_blueprint(modules_bp)

    from app.views.support import bp as support_bp
    app.register_blueprint(support_bp)

    from app.views.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    @app.after_request
    def set_secure_headers(response):
        # Strict Content Security Policy
        csp = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "script-src 'self'; "
            "frame-ancestors 'none';"
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
