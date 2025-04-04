from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models.user import User
from .. import db, bcrypt
from functools import wraps

# Create blueprint for users with a route prefix
users_bp = Blueprint('users', __name__, url_prefix='/users')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.order_by(User.id).all()
    return render_template('users.html', users=users)

@users_bp.route('/create-user', methods=['POST'])
@login_required
@admin_required
def create_user_route():
    if not all(k in request.form for k in ['username', 'password']):
        abort(400)

    # Get is_admin value, default to False if not present
    is_admin = request.form.get('is_admin', '0') == '1'

    # Generate password hash using bcrypt
    hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    
    new_user = User(
        email=request.form['username'],
        password_hash=hashed_pw,
        is_admin=is_admin
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('Username already taken or another error occurred', 'error')
    return redirect(url_for('users.index'))

@users_bp.route('/change_role', methods=['POST'])
@login_required
@admin_required
def change_role():
    if not all(k in request.form for k in ['user_id', 'is_admin']):
        abort(400)
    
    user = User.query.get_or_404(request.form['user_id'])
    user.is_admin = bool(int(request.form['is_admin']))
    try:
        db.session.commit()
        flash('User role updated successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('Error updating user role', 'error')
    return redirect(url_for('users.index'))

@users_bp.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete_user():
    if 'user_id' not in request.form:
        abort(400)
    
    user = User.query.get_or_404(request.form['user_id'])
    if user.id == current_user.id:
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('users.index'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    except Exception:
        db.session.rollback()
        flash('Error deleting user', 'error')
    return redirect(url_for('users.index'))
