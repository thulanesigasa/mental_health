from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/exercises')
def exercises_hub():
    return render_template('tools/index.html')

@bp.route('/exercises/breathe')
def breathe():
    return render_template('tools/breathe.html')

@bp.route('/exercises/grounding')
def grounding():
    return render_template('tools/grounding.html')
