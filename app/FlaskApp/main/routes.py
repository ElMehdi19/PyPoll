from flask import Blueprint, request, render_template
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/Home')
def home():
    is_authenticated = 'authenticated' in request.cookies
    now = datetime.utcnow()
    return render_template('home.html', title='Home', is_authenticated=is_authenticated, now=now)

