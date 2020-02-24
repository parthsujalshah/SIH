from server import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)
    group_type = db.Column(db.String(60))
    message = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'group_type': self.group_type,
            'message': self.message
        }

    def __repr__(self):
        return f"Message('{self.sender_id}')"