from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.extensions import db
from app.models.journal import JournalEntry
from app.views.user import login_required

journal_bp = Blueprint('journal_bp', __name__, url_prefix='/journal')

@journal_bp.route('/')
@login_required
def index():
    entries = JournalEntry.query.filter_by(user_id=session['user_id']).order_by(JournalEntry.created_at.desc()).all()
    return render_template('journal/index.html', entries=entries)

@journal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash('Both title and content are required.', 'error')
        else:
            entry = JournalEntry(user_id=session['user_id'], title=title, content=content)
            db.session.add(entry)
            db.session.commit()
            flash('Journal entry securely saved.', 'success')
            return redirect(url_for('journal_bp.index'))
    return render_template('journal/form.html', entry=None)

@journal_bp.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    # Strict IDOR / Authorization enforcement
    if entry.user_id != session['user_id']:
        flash('Unauthorized access strictly forbidden.', 'error')
        return redirect(url_for('journal_bp.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            flash('Both title and content are required.', 'error')
        else:
            entry.title = title
            entry.content = content
            db.session.commit()
            flash('Journal entry cleanly updated.', 'success')
            return redirect(url_for('journal_bp.index'))
    return render_template('journal/form.html', entry=entry)

@journal_bp.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != session['user_id']:
        flash('Unauthorized block.', 'error')
        return redirect(url_for('journal_bp.index'))
    db.session.delete(entry)
    db.session.commit()
    flash('Journal entry permanently deleted.', 'success')
    return redirect(url_for('journal_bp.index'))
