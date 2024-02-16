from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from .. import login_manager
from .helper_json import json_request, json_response
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, request
from ..models import User, BlockedUser, Product
from flask_login import current_user, login_user, login_required, logout_user

@api_bp.route('/users', methods=['GET'])
def get_user():
    filterName = request.args.get('name')
    result = User.get_filtered_by(name=filterName)
    # result = User.get(filterName)
    if result:
        data = User.to_dict(result)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found")
        return not_found("User not found")

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user_id(id):
    result = User.get(id)
    if result:
        data = User.to_dict(result)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found".format(id))
        return not_found("User not found")
    
@api_bp.route('/users/<int:id>/products', methods=['GET'])
def get_products_user(id):
    result = Product.get_all_filtered_by(seller_id=id)
    if result:
        (product) = result
        data = Product.to_dict_collection(product)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found".format(id))
        return not_found("User not found")


@api_bp.route('/users/login', methods=['POST'])
def login():
    
    data = request.get_json()
    
    if not data or 'name' not in data or 'password' not in data:
        return bad_request("Name and password are required in JSON data")
    name = data['name']
    plain_text_password = data['password']
    user = load_user(name)
   
    if user and check_password_hash(user.password, plain_text_password) and user.verified == 'true' :
        login_user(user)
        return json_response(data)
    if user:
        if user.verified != 'true' :
            return bad_request("User not verified")
        elif not check_password_hash(user.password, plain_text_password):
            return bad_request("Name and password do not match")
    return not_found("User not found")



@login_manager.user_loader
def load_user(name):
    if name is not None:
        # select amb 1 resultat o cap
        user_or_none =  User.get_filtered_by(name=name)
        return user_or_none
    return None