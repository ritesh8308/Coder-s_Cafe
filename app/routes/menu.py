from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.models.models import MenuItem
from app.forms.menu_form import MenuForm

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['GET', 'POST'])
def menu():
    form = MenuForm()

    if form.validate_on_submit():
        new_item = MenuItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            is_available=form.is_available.data
        )
        db.session.add(new_item)
        db.session.commit()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "status": "success",
                "message": "Item added.",
                "item": {
                    "id": new_item.id,
                    "name": new_item.name,
                    "price": new_item.price,
                    "category": new_item.category,
                    "is_available": new_item.is_available
                }
            })
        else:
            flash('✅ Menu item added successfully!', 'success')
            return redirect(url_for('menu.menu'))

    items = MenuItem.query.all()
    return render_template('menu.html', form=form, items=items)


@menu_bp.route('/menu/edit/<int:item_id>', methods=['POST'])
def edit_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.name = request.form['name']
    item.price = float(request.form['price'])
    item.category = request.form['category']
    item.is_available = 'is_available' in request.form

    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "status": "success",
            "message": "Item updated.",
            "item": {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "category": item.category,
                "is_available": item.is_available
            }
        })
    else:
        flash('✏️ Menu item updated!', 'info')
        return redirect(url_for('menu.menu'))


@menu_bp.route('/menu/delete/<int:item_id>', methods=['POST'])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "status": "success",
            "message": "Item deleted.",
            "item_id": item_id
        })
    else:
        flash('🗑️ Menu item deleted!', 'warning')
        return redirect(url_for('menu.menu'))
