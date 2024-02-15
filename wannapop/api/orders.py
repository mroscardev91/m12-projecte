from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import current_app, jsonify

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
def accept_order(order_id):
    order = Order.query.get(order_id)

    if order:
        if order.confirmed_order:
            return bad_request('Order already confirmed')

        confirmed_order = ConfirmedOrder(order=order)

        try:
            confirmed_order.save()
        except:
            return bad_request('Error confirming the order')

        current_app.logger.debug(f"Order {order_id} confirmed successfully")
        return jsonify(
            {   
                'data': order_id, 
                'success': True
            }), 200 
    else:
        return jsonify(
            {
                'error': 'Not Found', 
                'message': 'Order not found', 
                'success': False
            }), 404

@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
def cancel_confirmed_order(order_id):
    confirmed_order = ConfirmedOrder.query.get(order_id)

    if confirmed_order:
        # Elimina la entrada de confirmed_orders
        try:
            confirmed_order.delete()
        except:
            return bad_request('Error canceling the confirmed order')

        current_app.logger.debug(f"ConfirmedOrder {order_id} canceled successfully")
        return jsonify(
            {
                'data': order_id, 
                'success': True
            }), 200  
    else:
        return jsonify(
            {
                'error': 'Not Found', 
                'message': 'ConfirmedOrder not found', 
                'success': False
            }), 404