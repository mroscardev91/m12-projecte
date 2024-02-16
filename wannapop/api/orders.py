from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from .. import db_manager as db
from ..models import Order, User, ConfirmedOrder, Product
from .helper_json import json_request, json_response
from .helper_auth import basic_auth, token_auth
from flask import current_app, jsonify

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
@token_auth.login_required
def accept_order(order_id):
    order = Order.query.get(order_id)

    if order:

        product = Product.get(order.product_id)
        
        confirmed_order = ConfirmedOrder.get(id)
        if basic_auth.current_user().id == product.seller_id  :
            if confirmed_order :
                confirmed_order = ConfirmedOrder.create(order_id=id)
                data = ConfirmedOrder.to_dict(confirmed_order)
                return json_response(data)
            else:
                return bad_request("Order already confirmed")
        else:
            return forbidden_access("You are not the owner of this product")
        
    else:
        return not_found("Item not found")



@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
@token_auth.login_required
def cancel_confirmed_order(order_id):
    order = Order.get(id)
    confirmed_order = ConfirmedOrder.get(id)
    if confirmed_order:
        product = Product.get(order.product_id)
        if basic_auth.current_user().id == product.seller_id :
            confirmed_order.delete()
            return json_response(order.to_dict())
        else:
            return forbidden_access("You are not the owner of this product")
    else:
        return not_found("Order not found")