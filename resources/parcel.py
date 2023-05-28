from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ParcelModel
from schemas import ParcelSchema

blp = Blueprint("Parcels", __name__, description="Operations on parcel")


@blp.route("/parcel/<string:parcel_id>")
class Item(MethodView):
    @blp.response(200, ParcelSchema)
    def get(self, parcel_id):
        parcels = ParcelModel.query.filter_by(uid=str(parcel_id)).first()
        return parcels
