from db import db


class ParcelModel(db.Model):
    __tablename__ = "parcels"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String, unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False)
    pci_area = db.Column(db.Float(precision=2), unique=False, nullable=False)
    city_code = db.Column(db.String, unique=False, nullable=False)
    prefix_code = db.Column(db.String, unique=False, nullable=False)
    label = db.Column(db.String, unique=False, nullable=False)
