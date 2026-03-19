from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from app.extensions import db
from app.models.user import User
from app.models.module import Module
from app.models.support import SupportResource

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash("Please log in to access the administrator dashboard.", "error")
            return redirect(url_for('auth.login'))
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            flash("Action forbidden. Administrator level authorization required.", "error")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    modules = Module.query.all()
    resources = SupportResource.query.all()
    return render_template('admin/dashboard.html', modules=modules, resources=resources)

@bp.route('/module/new', methods=['GET', 'POST'])
@admin_required
def module_create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        if title and content:
            mod = Module(title=title, description=description, content=content)
            db.session.add(mod)
            db.session.commit()
            flash("Successfully created module.", "success")
            return redirect(url_for('admin.dashboard'))
        flash("Title and Content are required fields.", "error")
    return render_template('admin/form.html', entity_type='Module', action_url=url_for('admin.module_create'))

@bp.route('/module/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def module_edit(id):
    mod = Module.query.get_or_404(id)
    if request.method == 'POST':
        mod.title = request.form.get('title')
        mod.description = request.form.get('description')
        mod.content = request.form.get('content')
        db.session.commit()
        flash("Module successfully updated.", "success")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/form.html', entity_type='Module', action_url=url_for('admin.module_edit', id=id), entity=mod)

@bp.route('/module/delete/<int:id>', methods=['POST'])
@admin_required
def module_delete(id):
    mod = Module.query.get_or_404(id)
    db.session.delete(mod)
    db.session.commit()
    flash("Module permanently deleted.", "success")
    return redirect(url_for('admin.dashboard'))

@bp.route('/support/new', methods=['GET', 'POST'])
@admin_required
def support_create():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone_number')
        description = request.form.get('description')
        if name and phone:
            res = SupportResource(name=name, phone_number=phone, description=description)
            db.session.add(res)
            db.session.commit()
            flash("Successfully created support resource.", "success")
            return redirect(url_for('admin.dashboard'))
        flash("Name and Phone Number are required fields.", "error")
    return render_template('admin/form.html', entity_type='Support Resource', action_url=url_for('admin.support_create'))

@bp.route('/support/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def support_edit(id):
    res = SupportResource.query.get_or_404(id)
    if request.method == 'POST':
        res.name = request.form.get('name')
        res.phone_number = request.form.get('phone_number')
        res.description = request.form.get('description')
        db.session.commit()
        flash("Support Resource successfully updated.", "success")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/form.html', entity_type='Support Resource', action_url=url_for('admin.support_edit', id=id), entity=res)

@bp.route('/support/delete/<int:id>', methods=['POST'])
@admin_required
def support_delete(id):
    res = SupportResource.query.get_or_404(id)
    db.session.delete(res)
    db.session.commit()
    flash("Support Resource permanently deleted.", "success")
    return redirect(url_for('admin.dashboard'))
