from app.extensions import db
from datetime import datetime
from app.utils.security import verify_password

user_modules = db.Table('user_modules',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
)

user_resources = db.Table('user_resources',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('support_resource.id'), primary_key=True)
)

class MoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False, server_default='0')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    completed_modules = db.relationship('Module', secondary=user_modules, lazy='subquery',
        backref=db.backref('users_completed', lazy=True))
    bookmarked_resources = db.relationship('SupportResource', secondary=user_resources, lazy='subquery',
        backref=db.backref('users_bookmarked', lazy=True))
    mood_logs = db.relationship('MoodLog', backref='user', lazy=True, order_by='MoodLog.timestamp.desc()', cascade="all, delete-orphan")
    journal_entries = db.relationship('JournalEntry', backref='user', lazy=True, order_by='JournalEntry.created_at.desc()', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.email}>'

    def check_password(self, password):
        return verify_password(self.password_hash, password)
