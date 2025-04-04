from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

# Create blueprint for public
public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    # If user is already logged in, redirect to documents page
    if current_user.is_authenticated:
        return redirect(url_for('documents.index'))
    # Otherwise, show the public page
    return render_template('public/index.html')
