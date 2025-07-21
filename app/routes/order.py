from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import MenuItem, Order, OrderItem
from flask import make_response
from weasyprint import HTML

order_bp = Blueprint('order', __name__)

@order_bp.route('/order', methods=['GET', 'POST'])
def create_order():
    menu_items = MenuItem.query.filter_by(is_available=True).all()

    if request.method == 'POST':
        table_number = int(request.form['table_number'])
        new_order = Order(table_number=table_number, status='pending')
        db.session.add(new_order)
        db.session.commit()

        # Parse selected items
        for item in menu_items:
            qty = int(request.form.get(f'quantity_{item.id}', 0))
            if qty > 0:
                order_item = OrderItem(order_id=new_order.id, menu_item_id=item.id, quantity=qty)
                db.session.add(order_item)

        db.session.commit()
        flash("✅ Order placed successfully!", "success")
        return redirect(url_for('order.order_success', order_id=new_order.id))
    return render_template('order.html', menu_items=menu_items)

@order_bp.route('/order/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order.id).all()

    # Calculate total
    total_amount = 0
    item_details = []
    for i in items:
        menu_item = MenuItem.query.get(i.menu_item_id)  # or i.menu_item if relationship is set
        item_total = menu_item.price * i.quantity
        total_amount += item_total
        item_details.append({
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": i.quantity,
            "subtotal": item_total
        })
    return render_template('order_success.html', order=order, items=item_details, total=total_amount)


@order_bp.route('/invoice/<int:order_id>')
def invoice_preview(order_id):
    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order.id).all()

    total_amount = 0
    item_details = []
    for i in items:
        menu_item = MenuItem.query.get(i.menu_item_id)
        item_total = menu_item.price * i.quantity
        total_amount += item_total
        item_details.append({
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": i.quantity,
            "subtotal": item_total
        })

    return render_template('invoice.html',
                           order=order,
                           items=item_details,
                           total=total_amount)


@order_bp.route('/invoice/<int:order_id>/download')
def download_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    items = OrderItem.query.filter_by(order_id=order.id).all()

    total_amount = 0
    item_details = []
    for i in items:
        menu_item = MenuItem.query.get(i.menu_item_id)
        item_total = menu_item.price * i.quantity
        total_amount += item_total
        item_details.append({
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": i.quantity,
            "subtotal": item_total
        })

    html = render_template("invoice.html", order=order, items=item_details, total=total_amount)
    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = f"invoice_{order.id}_table{order.table_number}_{order.created_at.strftime('%Y%m%d_%H%M')}.pdf"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'

    return response


    return render_template('order_success.html', order=order, items=item_details, total=total_amount)

