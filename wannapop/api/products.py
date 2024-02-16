from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from .. import db_manager as db
from ..models import Product, Category, Order
from .helper_json import json_request, json_response
from .helper_auth import basic_auth, token_auth
from flask import current_app, jsonify, request

#List
@api_bp.route('/products', methods=['GET'])
def get_product_filtred():
    title = request.args.get('title')
    if title:
        Product.db_enable_debug()
        products_with_title = Product.query.filter_by(title=title).all()
    else:
        products_with_title = []
    data = Product.to_dict_collection(products_with_title)
    return jsonify(
        {
            'data': data, 
            'success': True
        }), 200
    

@api_bp.route('/products/<int:product_id>/orders', methods=['GET'])
def listar_ofertas_por_producto(product_id):
    orders = Order.query.filter_by(product_id=product_id).all()
    if orders:
        data = [order.to_dict() for order in orders]
        return jsonify(
        {
            'data': data, 
            'success': True
        }), 200  
    else:
        return not_found('No offers found for the specified product')

#Show
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_api_product_show(id):
    result = Product.get_with(id, Category)
    if result:
        (product, category) = result
        # Serialize data
        data = product.to_dict()
        # Add relationship
        data["category"] = category.to_dict()
        del data["category_id"]
        return jsonify(
            {
                'data': data, 
                'success': True
            }), 200  
    else:
        current_app.logger.debug(f"Product {id} not found")
        return not_found("Product not found")

# Update
@api_bp.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_api_product(id):
    product = Product.get(id)
    if basic_auth.current_user().id == product.seller_id :
        data = json_request(['title','description', 'photo', 'price'],False)
        current_app.logger.debug(data)
        product.update(**data)
        return json_response(product.to_dict())
    else: 
        return forbidden_access("You are not the owner of this product")