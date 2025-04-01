from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt
from models import User
from extensions import db

from app import admin_required, bcrypt

users_bp = Blueprint('users', __name__)

@users_bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id).all()
    return render_template('users.html', users=users)

@users_bp.route('/create-user', methods=['POST'])
@login_required
@admin_required
def create_user_route():
    if not all(k in request.form for k in ['username', 'password', 'role']):
        abort(400)

    hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    new_user = User(
        username=request.form['username'],
        password=hashed_pw,
        role=request.form['role'],
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name')
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Kullanıcı başarıyla oluşturuldu', 'success')
    except Exception:
        db.session.rollback()
        flash('Bu kullanıcı adı zaten alınmış veya başka bir hata oluştu', 'error')
    return redirect(url_for('users.admin_users'))

@users_bp.route('/admin/users/change_role', methods=['POST'])
@login_required
@admin_required
def change_role():
    user_id = request.form.get('user_id', '').strip()
    new_role = request.form.get('role', 'user').strip()
    if not user_id:
        flash('Kullanıcı ID eksik', 'error')
        return redirect(url_for('users.admin_users'))

    try:
        user = User.query.get(int(user_id))
        if user:
            user.role = new_role
            db.session.commit()
            flash('Kullanıcı rolü güncellendi', 'success')
        else:
            flash('Kullanıcı bulunamadı', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Kullanıcı rolü güncelleme hatası: ' + str(e), 'error')

    return redirect(url_for('users.admin_users'))

@users_bp.route('/admin/users/delete', methods=['POST'])
@login_required
@admin_required
def delete_user():
    user_id = request.form.get('user_id', '').strip()
    if not user_id:
        flash('Kullanıcı ID bulunamadı', 'error')
        return redirect(url_for('users.admin_users'))

    if user_id == str(current_user.id):
        flash('Kendi hesabınızı silemezsiniz!', 'error')
        return redirect(url_for('users.admin_users'))

    try:
        user = User.query.get(int(user_id))
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Kullanıcı silindi', 'success')
        else:
            flash('Kullanıcı bulunamadı', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Kullanıcı silme hatası: ' + str(e), 'error')

    return redirect(url_for('users.admin_users'))
