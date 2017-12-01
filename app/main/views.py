from . import main
from flask import session, render_template


@main.route('/')
def index():
    user = unicode(session.get('login_id', ''))
    return render_template('cover.html', user=user)