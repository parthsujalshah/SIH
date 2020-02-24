from server import db, app, login, admin, current_user

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(60), unique=True, nullable=False)
    pan_image_base64 = db.Column(db.Text)
    soil_card_image_base64 = db.Column(db.Text)
    field_area = db.Column(db.String(20))
    location = db.Column(db.String(20))
    machinery_owned = db.Column(db.String(60))
    crops = db.relationship('Crop', backref='owner', lazy=True)
    messages = db.relationship('Message', backref='message_sender', lazy=True)

    def to_dict_for_selling(self):
        crops_for_sale= []
        for crop in self.crops:
            if crop.is_selling:
                crops_for_sale.append(crop.to_dict())
        if crops_for_sale != []:
            return {
                'id': self.id,
                'name': self.name,
                'phone_number': self.phone_number,
                'crops_for_sale': crops_for_sale
            }
        else:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'machinery_owned': self.machinery_owned
        }

    def __repr__(self):
        return f"Farmer('{self.name}', '{self.phone_number}, '{self.machinery_owned}')"