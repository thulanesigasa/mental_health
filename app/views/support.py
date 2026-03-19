from flask import Blueprint, render_template
from app.models.support import SupportResource

bp = Blueprint('support', __name__, url_prefix='/support')

@bp.route('/')
def directory():
    resources = SupportResource.query.order_by(SupportResource.name.asc()).all()
    return render_template('support/directory.html', resources=resources)
