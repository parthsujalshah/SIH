from server import app, db
from server.models import Farmer, Scheme
from flask import request, jsonify, Blueprint
from server.static.utils import token_required
from werkzeug.security import generate_password_hash, check_password_hash
import nexmo
# from server.static.fertilizer_prediction import fertilizer_prediction
import jwt

farmers_routes = Blueprint('farmer_routes', __name__)

@farmers_routes.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    username = request.json.get('name', None)
    phone_number = request.json.get('phone_number', None)
    password = username + phone_number[-4:]
    hashed_password = generate_password_hash(password)
    image_base64 = request.json.get('pan_image_base64', None)
    soil_card_image_base64 = request.json.get('soil_card_image_base64', None)
    location = request.json.get('location', None)
    field_area = request.json.get('field_area', None)
    machinery_owned = request.json.get('machinery', None)
    farmer = Farmer(
        name = username,
        password = hashed_password,
        phone_number = phone_number,
        pan_image_base64 = image_base64,
        soil_card_image_base64 = soil_card_image_base64,
        location = location,
        field_area = field_area,
        machinery_owned = machinery_owned,
    )
    db.session.add(farmer)
    db.session.commit()
    client = nexmo.Client(key=app.config['API_KEY'], secret=app.config['API_SECRET_KEY'])
    client.send_message({
        'from': 'Nexmo',
        'to': '918920278726',
        # 'text': f'Class of fertilizer: {fertilizer_prediction.fertilizer_prediction([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])}',
        'text': 'Class of fertilizer:',
    })
    return jsonify({'password': password})

@farmers_routes.route('/login', methods=['GET', 'POST'])
def login():
    if not request.json.get('name') or not request.json.get('password'):
        return jsonify({'message': 'Could not verify'}), 401
    farmer = Farmer.query.filter_by(name=request.json.get('name')).first()

    if not farmer:
        return jsonify({'message': 'Could not verify'}), 401
    if check_password_hash(farmer.password, request.json.get('password')):
        token = jwt.encode(
            {
                'farmer_id': farmer.id,
                'username': farmer.name,
            },
            app.config['SECRET_KEY']
        )  # Save this in async storage in app
        return jsonify({'token': token.decode('UTF-8')})
    return jsonify({'message': 'Could not verify'}), 401

@farmers_routes.route('/logout', methods=['GET', 'POST'])
@token_required
def logout(current_user):
    loggin_out = request.json.get('loggin_out')
    return jsonify({'logged_in': False})

@farmers_routes.route('/show_schemes', methods=['GET', 'POST'])
@token_required
def show_schemes(current_user):
    schemes_list = []
    schemes = Scheme.query.all()
    for scheme in schemes:
        schemes_list.append(scheme.to_dict())
    return jsonify({'schemes': schemes_list})