from server import app, db
from server.models import Crop
from flask import jsonify, request, Blueprint
from server.static.utils import token_required, save_image
import threading
import time
# from server.static.utils import seed_required, fertilizer_required
# from server.crops.utils import suggestions, alerts

crops_routes = Blueprint('crops_routes', __name__)

@crops_routes.route('/add_crop', methods=['GET', 'POST'])
@token_required
def add_crop(current_user):
    crop_name = request.json.get('crop_name', None)
    crop = Crop(crop_name=crop_name, owner=current_user)
    # seed_required(float(current_user.field_area))
    # fertilizer_required(float(current_user.field_area))
    # Timer
    thread = threading.Thread(target=suggestions)
    thread.daemon = True
    thread.start()
    days = 1
    thread = threading.Thread(target=alerts, args=(current_user, days,))
    thread.daemon = True
    thread.start()
    # Timer
    db.session.add(crop)
    db.session.commit()
    return jsonify({'message': 'crop_added'})

@crops_routes.route('/show_crops', methods=['GET', 'POST'])
@token_required
def show_crops(current_buyer):
    crop_list = []  
    for crop in Crop.query.all():
        crop_list.append(crop.to_dict())
    return jsonify({'crops_list': crop_list})

@crops_routes.route('/sell', methods=['GET', 'POST'])
@token_required
def sell(current_user):
    added = request.json.get('added', None)
    if added:
        crop_name = request.json.get('crop_name', None)
        price_per_kg = request.json.get('price_per_kg', None)
        selling_crop_kg = request.json.get('selling_crop_kg', None)
        selling_crop_image_base64 = request.json.get('selling_crop_image_base64', None)
        crop = Crop.query.filter_by(crop_name=crop_name)
        crop.price_per_kg = price_per_kg
        crop.selling_crop_kg = selling_crop_kg
        crop.selling_crop_image_base64 = selling_crop_image_base64
        crop.is_selling = True
        db.session.commit()
    else:
        crop_name = request.json.get('crop_name', None)
        price_per_kg = request.json.get('price_per_kg', None)
        selling_crop_kg = request.json.get('selling_crop_kg', None)
        selling_crop_image_base64 = request.json.get('selling_crop_image_base64', None)
        crop = Crop(
            crop_name = crop_name,
            price_per_kg = price_per_kg,
            selling_crop_kg = selling_crop_kg,
            selling_crop_image_base64 = selling_crop_image_base64,
            is_selling = True,
            owner = current_user
        )
        db.session.add(crop)
        db.session.commit()
    return jsonify({'message': 'Added to selling list'})

@crops_routes.route('/disease_check', methods=['GET', 'POST'])
@token_required
def disease_check(current_user):
    image_base64 = request.json.get('image', None)
    save_image(image_base64)
    # im1 = Image.open(r"D:\Documents\Projects\AppDevelopment\SIH\Server\server\static\images\a.png")
    # print(disease(im1))
    healthy = False
    return jsonify({'healthy': healthy})