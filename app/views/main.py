from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/tools/breathe')
def breathe():
    return render_template('tools/breathe.html')

@bp.route('/tools/grounding')
def grounding():
    return render_template('tools/grounding.html')
