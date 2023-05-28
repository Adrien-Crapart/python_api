from flask import request
from flask.views import MethodView
from flask_uploads import UploadNotAllowed
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from libs import image_helper
# from libs.strings import gettext
from models import ItemModel
from schemas import ImageSchema


blp = Blueprint("Images", __name__, description="Operations on image")

image_schema = ImageSchema()


@blp.route("/image/<int:item_id>")
class ImageUpload(MethodView):
    @jwt_required()
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": f"Image {basename} uploaded."}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": f"Extension '{extension}' is not allowed."}, 400
