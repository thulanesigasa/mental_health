from flask import Blueprint, render_template, make_response, request, url_for
from app.models.module import Module
import datetime

seo_bp = Blueprint('seo', __name__)

@seo_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml dynamically scaling across native DB module hooks."""
    pages = []
    # Static pages
    ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).date().isoformat()
    # Explicitly omitting /tools/grounding since it isn't registered yet! I'll add it later or omit it temporarily.
    for rule in ['main.index', 'support.directory', 'auth.login', 'auth.register', 'main.breathe']:
        url = url_for(rule, _external=True)
        pages.append([url, ten_days_ago])
        
    modules = Module.query.all()
    for module in modules:
        url = url_for('modules.detail', module_id=module.id, _external=True)
        pages.append([url, ten_days_ago])

    sitemap_xml = render_template('seo/sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@seo_bp.route('/robots.txt')
def robots():
    """Generate robots.txt securely preventing restricted area spider mapping."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /user/",
        "Disallow: /journal/",
        f"Sitemap: {url_for('seo.sitemap', _external=True)}"
    ]
    response = make_response("\n".join(lines))
    response.headers["Content-Type"] = "text/plain"
    return response
