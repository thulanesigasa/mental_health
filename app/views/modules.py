from flask import Blueprint, render_template, session
from app.models.module import Module
from app.models.user import User

bp = Blueprint('modules', __name__, url_prefix='/modules')

@bp.route('/')
def list_modules():
    modules = Module.query.order_by(Module.id.asc()).all()
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('modules/list.html', modules=modules, user=user)

@bp.route('/<int:module_id>')
def detail(module_id):
    module = Module.query.get_or_404(module_id)
    next_module = Module.query.filter(Module.id > module_id).order_by(Module.id.asc()).first()
    return render_template('modules/detail.html', module=module, next_module=next_module)
