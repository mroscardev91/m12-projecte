from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Product, Category, Order
from ..helper_json import json_request, json_response
from flask import current_app

#List
@api_bp.route('/products', methods=['GET'])
def get_product_filtered():
    product_with_categories = Product.get_all_with(Category)
    data = Product.to_dict_collection(product_with_categories)

    response = {
        "data": data,
        "success": True
    }

    return json_response(response)

@api_bp.route('/products/<int:product_id>/orders', methods=['GET'])
def listar_ofertas_por_producto(product_id):
    orders = Order.query.filter_by(product_id=product_id).all()
    if orders:
        data = [order.to_dict() for order in orders]
        return json_response(data)
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
        return json_response(data)
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")

# Update
@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_api_product(id):
    product = Product.get(id)
    if product:
        try:
            data = json_request(['title', 'description', 'photo', 'price', 'category_id'], False)
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            product.update(**data)
            current_app.logger.debug("UPDATED item: {}".format(product.to_dict()))
            return json_response(product.to_dict())
    else:
        current_app.logger.debug("Product {} not found".format(id))
        return not_found("Product not found")