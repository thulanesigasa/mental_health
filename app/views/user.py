import datetime
import io
import csv
import json
from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response, request
from functools import wraps
from datetime import datetime, timedelta
from app.extensions import db
from app.models.user import User, MoodLog
from app.models.journal import JournalEntry
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
    # Secure Analytics Range Mapping
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_moods = MoodLog.query.filter(
        MoodLog.user_id == user.id,
        MoodLog.timestamp >= seven_days_ago
    ).order_by(MoodLog.timestamp.asc()).all()
    
    return render_template('user/dashboard.html', logs=recent_moods, user=user) # Adjusted to pass existing recent_moods as 'logs' for consistency with instruction's template variables

@user_bp.route('/export')
@login_required
def export_data():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    # Fetch data
    mood_logs = MoodLog.query.filter_by(user_id=user_id).order_by(MoodLog.timestamp.asc()).all()
    journal_entries = JournalEntry.query.filter_by(user_id=user_id).order_by(JournalEntry.created_at.asc()).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Mood Logs Header and Data
    writer.writerow(['--- MOOD LOGS ---'])
    writer.writerow(['Date', 'Mood Value', 'Note'])
    for log in mood_logs:
        writer.writerow([log.timestamp.strftime('%Y-%m-%d %H:%M:%S'), log.score, log.note if hasattr(log, 'note') else '']) # Assuming MoodLog has a 'score' and potentially 'note'
    
    writer.writerow([]) # Spacer
    
    # Journal Entries Header and Data
    writer.writerow(['--- JOURNAL ENTRIES ---'])
    writer.writerow(['Date', 'Title', 'Content'])
    for entry in journal_entries:
        writer.writerow([entry.created_at.strftime('%Y-%m-%d %H:%M:%S'), entry.title, entry.content])
        
    output.seek(0)
    
    response = make_response(output.getvalue())
    filename = f"serenity_data_export_{datetime.now().strftime('%Y%m%d')}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    
    return response

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

@user_bp.route('/log_mood', methods=['POST'])
@login_required
def log_mood():
    user = User.query.get(session['user_id'])
    score = request.form.get('score', type=int)
    if score and 1 <= score <= 5:
        log = MoodLog(user_id=user.id, score=score)
        db.session.add(log)
        db.session.commit()
        flash('Mood securely logged for today.', 'success')
    else:
        flash('Invalid mood score submitted.', 'error')
    return redirect(url_for('user_bp.dashboard'))
