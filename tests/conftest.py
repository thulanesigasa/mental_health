import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    from app.utils.security import hash_password
    hashed_pw = hash_password('initial_secure_pass_123')
    user = User(email='test@example.com', password_hash=hashed_pw)
    admin = User(email='admin@example.com', password_hash=hashed_pw, is_admin=True)
    db.session.add(user)
    db.session.add(admin)
    db.session.commit()
    return db
