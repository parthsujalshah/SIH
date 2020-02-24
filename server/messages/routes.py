from server import app, db
from server.messages.models import Message
from server.farmers.models import Farmer
from flask import jsonify, request, Blueprint
from server.static.utils import token_required

message_routes = Blueprint('message_routes', __name__)

@message_routes.route('/show_messages/<group_type>', methods=['GET', 'POST'])
@token_required
def show_messages_machinery(current_user, group_type):
    messages = []
    for message in Message.query.all():
        if message.group_type == group_type:
            is_sender = False
            if message.sender_id == current_user.id:
                is_sender = True
            messages.append({
                'sender': Farmer.query.get(message.sender_id).to_dict(),
                'message': message.message,
                'is_sender': is_sender
            })
    return jsonify({'message_list': messages})

@message_routes.route('/add_message', methods=['GET', 'POST'])
@token_required
def add_message(current_user):
    message = request.json.get('message')
    group_type = request.json.get('group_type')
    new_message = Message(
        message = message,
        message_sender = current_user,
        group_type = group_type
    )
    new_message.message_sender = current_user
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'message added'})