from flask import Blueprint, render_template
from flask_login import login_required

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/favorite_characters')
@login_required
def favorite_characters():
    return render_template('favorite_characters.html')

@site.route('/favorite_comics')
@login_required
def favorite_comics():
    return render_template('favorite_comics.html')