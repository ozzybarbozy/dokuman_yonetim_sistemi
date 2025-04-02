from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from extensions import db, bcrypt
from models import User
from app import log_activity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('documents.documents'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            log_activity('login')
            return redirect(url_for('documents.documents'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    log_activity('logout')
    logout_user()
    return redirect(url_for('auth.login'))
