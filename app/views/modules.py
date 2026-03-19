from flask import Blueprint, render_template
from app.models.module import Module

bp = Blueprint('modules', __name__, url_prefix='/modules')

@bp.route('/')
def list_modules():
    modules = Module.query.order_by(Module.created_at.desc()).all()
    # If no modules, we can create some dummy ones or just render empty
    return render_template('modules/list.html', modules=modules)

@bp.route('/<int:module_id>')
def detail(module_id):
    module = Module.query.get_or_404(module_id)
    return render_template('modules/detail.html', module=module)
