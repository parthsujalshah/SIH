from functools import wraps
import os
import secrets
from PIL import Image
from io import BytesIO
import base64
import threading
import time
import nexmo
from server import app
from flask import request, jsonify
from server.models import Farmer, Buyer
import jwt
import nexmo


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            _id = data['farmer_id']
            current_user = Farmer.query.get(_id)
        except:
            return jsonify({'message': 'Token is Invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/gov_id', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_image(base64_image):
    png_bytes = base64.b64decode(base64_image)
    stream = BytesIO(png_bytes)
    image = Image.open(stream).convert("RGBA")
    picture_fn = 'a.png'
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    image.save(picture_path)
    stream.close()

def token_buyer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            _id = data['buyer_id']
            current_buyer = Buyer.query.get(_id)
        except:
            return jsonify({'message': 'Token is Invalid!'}), 401
        return f(current_buyer, *args, **kwargs)
    return decorated