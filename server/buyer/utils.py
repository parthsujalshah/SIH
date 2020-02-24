from functools import wraps
from flask import request, jsonify
import jwt
from server.buyer.models import Buyer

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