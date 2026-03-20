from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from functools import wraps
from app.extensions import db
from app.models.user import User
from app.models.module import Module
from app.models.support import SupportResource

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access your dashboard.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('user/dashboard.html', user=user)

@user_bp.route('/bookmark/<int:resource_id>', methods=['POST'])
@login_required
def bookmark_resource(resource_id):
    user = User.query.get(session['user_id'])
    resource = SupportResource.query.get_or_404(resource_id)
    if resource in user.bookmarked_resources:
        user.bookmarked_resources.remove(resource)
        flash('Support contact removed from bookmarks.', 'success')
    else:
        user.bookmarked_resources.append(resource)
        flash('Support contact securely bookmarked!', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('user_bp.dashboard'))

@user_bp.route('/complete/<int:module_id>', methods=['POST'])
@login_required
def complete_module(module_id):
    user = User.query.get(session['user_id'])
    module = Module.query.get_or_404(module_id)
    if module not in user.completed_modules:
        user.completed_modules.append(module)
        flash('Module specifically marked as completed! Great progress.', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('user_bp.dashboard'))
