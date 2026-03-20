from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.extensions import db, limiter, mail
from app.models.user import User
from app.utils.security import hash_password
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('auth/register.html')
            
        try:
            hashed_pw = hash_password(password)
            user = User(email=email, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email is already registered.', 'error')
            
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
            
        flash('Invalid email or password.', 'error')
        
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if session.get('user_id'):
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate secure token
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            # Send email
            msg = Message('Password Reset - Serenity',
                          recipients=[user.email])
            msg.body = f"To reset your password, visit the following securely encrypted link:\n{reset_url}\n\nIf you did not make this request, simply ignore this email."
            
            # If MAIL_SERVER is localhost, it'll fail without smtpd. We use try/except to simulate success in dev.
            try:
                mail.send(msg)
            except ConnectionRefusedError:
                # Fallback for local dev without SMTP server running
                print(f"DEV MODE: Email meant for {user.email}\n{msg.body}")
            
        flash('Check your email for precise instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password_request.html')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if session.get('user_id'):
        return redirect(url_for('main.index'))
        
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is entirely invalid or has expired.', 'error')
        return redirect(url_for('auth.reset_password_request'))
        
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user:
            password = request.form.get('password')
            if password:
                user.password_hash = hash_password(password)
                db.session.commit()
                flash('Your password has been reset securely.', 'success')
                return redirect(url_for('auth.login'))
            flash('Password cannot be empty.', 'error')
    return render_template('auth/reset_password.html')
