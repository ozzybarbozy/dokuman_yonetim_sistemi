from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db, bcrypt
from ..models.user import User
from functools import wraps

users_bp = Blueprint('users_bp', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin privileges required', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@users_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('users_bp.add_user'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('User added successfully', 'success')
        return redirect(url_for('users_bp.list_users'))
        
    return render_template('users/add.html')

@users_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.rank = request.form.get('rank')
        user.phone_number = request.form.get('phone_number')
        
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('users_bp.list_users'))
        
    return render_template('users/edit.html', user=user)

@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    if current_user.id == id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('users.list_users'))
        
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('users.list_users'))

@users_bp.route('/users/create', methods=['POST'])
@login_required
def create_user_route():
    # Logic to create a new user
    pass

@users_bp.route('/users/delete', methods=['POST'])
@login_required
def delete_user_post():
    # Logic to delete a user
    pass

@users_bp.route('/users/change-role', methods=['POST'])
@login_required
def change_role():
    # Logic to change user role
    pass
