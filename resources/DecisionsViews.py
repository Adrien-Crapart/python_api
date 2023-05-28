from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from libs import DecisionsControllers

from db import db
from models import ItemModel
from schemas import DecisionsSchema

blp = Blueprint("Decisions", __name__, description="Operations on decisions")


@blp.route("/filter-viewer/<string:table>")
class Filter(MethodView):

    @blp.response(200, DecisionsSchema)
    def get(self, table):
        try:
            items = DecisionsControllers.get_delta_info(table)
            return jsonify(items), 200
        except KeyError:
            abort(404, message="Aucun résultat trouvé")


@blp.route('/days_by_month/<int:year>/<int:month>')
class DaysConstruction(MethodView):

    @blp.response(200, DecisionsSchema)
    def get(year, month):
        try:
            items = DecisionsControllers.get_days_by_month(year, month)
            return jsonify(items), 200
        except KeyError:
            abort(404, message="Aucun résultat trouvé")


@blp.route('/<string:table>/items/<string:year>/<string:month>/<string:day>')
class Decisions(MethodView):

    @blp.response(200, DecisionsSchema)
    def get(table, year, month, day):
        try:
            items = DecisionsControllers.get_sumary_item(
                table, year, month, day)
            return jsonify(items), 200
        except KeyError:
            abort(204, message="Aucun résultat trouvé")


@blp.route("/<string:table>/item/<int:id>")
class DecisionsById(MethodView):

    @blp.response(200, DecisionsSchema)
    def get(table, id):
        item = DecisionsControllers.get_by_id(table, id)
        if item == []:
            return {"message": "Aucun résultat trouvé !", "type_error": 404}, 404
        return jsonify(item), 200

    def delete(table, id):
        result = DecisionsControllers.delete_item(table, id)
        if result is None:
            return {"message": "Erreur lors de la suppression !", "type_error": 404}, 404
        return jsonify(result), 201


@blp.route("/<string:table>/item")
class PostDecisions(MethodView):

    @blp.response(200, DecisionsSchema)
    def post(table):
        item = request.get_json()
        year = item["year"]
        month = item["month"]
        day = item["day"]
        file_name = item["day"]
        date = item["day"]
        text_list = item["day"]
        result = DecisionsControllers.insert_item(
            table, year, month, day, file_name, date, text_list)
        if result is None:
            return {"message": "L'insertion en base de donnée à échoué !"}, 404
        return jsonify(result), 201

    def put(table):
        item = request.get_json()
        id = item["id"]
        year = item["year"]
        month = item["month"]
        day = item["day"]
        file_name = item["day"]
        date = item["day"]
        text_list = item["day"]
        result = DecisionsControllers.update_item(
            table, id, year, month, day, file_name, date, text_list)
        if result is None:
            return {"message": "La modification de cette donnée à échoué !", "type_error": 404}, 404
        return jsonify(result), 201
