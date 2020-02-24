from server import db

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(120), nullable=False)
    selling_crop_kg = db.Column(db.String(120))
    selling_crop_image_base64 = db.Column(db.Text)
    price_per_kg = db.Column(db.String(60))
    is_selling = db.Column(db.Boolean, default=False)
    soil_card_image_base64 = db.Column(db.Text)
    sown = db.Column(db.Boolean, default=False)
    harvested = db.Column(db.Boolean, default=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'selling_crop_kg': self.selling_crop_kg,
            'price_per_kg': self.price_per_kg,
            'selling_crop_image_base64': self.selling_crop_image_base64
        }

    def __repr__(self):
        return f"Crop('{self.crop_name}', {self.farmer_id}, '{self.is_selling}')"