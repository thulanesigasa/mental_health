import random
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.forum import ForumPost

bp = Blueprint('forum', __name__)

ADJECTIVES = ["Calm", "Brave", "Quiet", "Bright", "Strong", "Kind", "Steady", "Wise", "Peaceful"]
NOUNS = ["Panda", "River", "Willow", "Mountain", "Starlight", "Ocean", "Oak", "Sunrise", "Breeze"]

def generate_pseudonym():
    return f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}"

@bp.route('/forum')
def index():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('forum/index.html', posts=posts)

@bp.route('/forum/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content are required.')
            return redirect(url_for('forum.create'))
            
        post = ForumPost(
            title=title,
            content=content,
            pseudonym=generate_pseudonym()
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created anonymously!')
        return redirect(url_for('forum.index'))
        
    return render_template('forum/create.html')
