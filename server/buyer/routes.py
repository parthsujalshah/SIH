from flask import request, jsonify,Blueprint
from server import app
from server.models import Buyer, Farmer
from werkzeug.security import check_password_hash
import jwt
from server.static.utils import token_buyer_required

buyer_routes = Blueprint('buyer_routes', __name__)


@buyer_routes.route('/buyer_login', methods=['GET', 'POST'])
def buyer_login():
    if not request.json.get('username') or not request.json.get('password'):
        return jsonify({'message': 'Could not verify 1st'}), 401
    buyer = Buyer.query.filter_by(username=request.json.get('username')).first()
    if not buyer:
        return jsonify({'message': 'Could not verify 2nd'}), 401
    if check_password_hash(buyer.password, request.json.get('password')):
        token = jwt.encode(
            {
                'buyer_id': buyer.id,
                'username': buyer.username,
            },
            app.config['SECRET_KEY']
        )  # Save this in async storage in app
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Could not verify 3rd'}), 401

@buyer_routes.route('/buyer_home', methods=['GET', 'POST'])
@token_buyer_required
def buyer_home(current_buyer):
    crops_array = []
    for farmer in Farmer.query.all():
        if farmer.to_dict_for_selling:
            crops_array.append(farmer.to_dict_for_selling())
    return jsonify({'crops_for_sale': crops_array})

@buyer_routes.route('/logout_buyer', methods=['GET', 'POST'])
@token_buyer_required
def logout_buyer(current_buyer):
    loggin_out = request.json.get('loggin_out')
    return jsonify({'logged_in': False})