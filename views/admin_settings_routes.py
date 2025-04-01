from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, abort
)
from flask_login import login_required, current_user
from models import Originator, DocumentType, Discipline, Category, BuildingCode
from extensions import db

settings_bp = Blueprint('admin_settings', __name__)

MODELS = {
    'originator': Originator,
    'document_type': DocumentType,
    'discipline': Discipline,
    'category': Category,
    'building_code': BuildingCode,
}

@settings_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if current_user.role != 'admin':
        abort(403)

    if request.method == 'POST':
        model_key = request.form.get('model')
        code = request.form.get('code', '').strip()
        description = request.form.get('description', '').strip()

        if model_key in MODELS and code and description:
            Model = MODELS[model_key]
            existing = Model.query.filter_by(code=code).first()
            if existing:
                flash(f"Aynı koda sahip bir kayıt zaten var: {code}", 'danger')
            else:
                entry = Model(code=code, description=description)
                db.session.add(entry)
                db.session.commit()
                flash(f"{model_key.replace('_', ' ').title()} eklendi.", 'success')
        return redirect(url_for('admin_settings.admin_settings'))

    all_data = {
        key: model.query.order_by(model.code).all()
        for key, model in MODELS.items()
    }

    return render_template('admin_settings.html', data=all_data)


@settings_bp.route('/admin/settings/delete/<model>/<int:item_id>', methods=['POST'])
@login_required
def delete_setting(model, item_id):
    if current_user.role != 'admin':
        abort(403)

    Model = MODELS.get(model)
    if not Model:
        abort(404)

    item = Model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Kayıt silindi.", "success")
    return redirect(url_for('admin_settings.admin_settings'))


@settings_bp.route('/admin/settings/update/<model>/<int:item_id>', methods=['POST'])
@login_required
def update_setting(model, item_id):
    if current_user.role != 'admin':
        abort(403)

    code = request.form.get('code', '').strip()
    description = request.form.get('description', '').strip()

    Model = MODELS.get(model)
    if not Model or not code or not description:
        abort(400)

    item = Model.query.get_or_404(item_id)
    item.code = code
    item.description = description
    db.session.commit()
    flash("Kayıt güncellendi.", "success")
    return redirect(url_for('admin_settings.admin_settings'))
