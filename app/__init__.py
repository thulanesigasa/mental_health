from flask import Flask, render_template
from config import Config
from app.extensions import db, migrate, limiter, mail

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    mail.init_app(app)

    # Import models so Alembic can discover them
    from app import models
    from app.models import journal

    # Register blueprints
    from app.views import main, auth, modules, support, admin, user, journal, seo, forum
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(modules.bp)
    app.register_blueprint(support.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(journal.journal_bp)
    app.register_blueprint(seo.seo_bp)
    app.register_blueprint(forum.bp)

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

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
