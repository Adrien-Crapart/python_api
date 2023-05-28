# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import jinja2

import jobs
import rq
from db import db
from blocklist import BLOCKLIST

# from resources.DecisionsViews import blp as DecisionsBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from resources.parcel import blp as ParcelBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    # jobs.rq.init_app(app)
    load_dotenv()

    app.config["PROPAGATE_EXECEPTIONS"] = True
    app.config["API_TITLE"] = "DATA REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite://database.db")
    app.config["SQLALCHEMY_TRACK_MODIFCATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # import secrets > secrets.SystemRandom().getrandbits(256)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token has been revoked.", "error": "token_revoked"}), 401)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}), 401)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Look in the database and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (jsonify({"message": "The token has expired.", "error": "token_expired"}), 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature failed.", "error": "invalid_token"}), 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}), 401)

    @app.before_first_request
    def create_tables():
        db.create_all()

    # api.register_blueprint(DecisionsBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ParcelBlueprint)

    # For sake of simplicty, we keep track of the jobs we've launched
    # in memory. This will only work as long there is only one python
    # process (web server context) and it must not get restarted.
    # In advanced use cases you want to keep track of jobs by their ids
    # and utilize sessions and redis.
    # joblist = []
    # template_loader = jinja2.FileSystemLoader("templates")
    # template_env = jinja2.Environment(loader=template_loader)

    # @app.route('/')
    # def index():
    #     l = []
    #     # work on copy of joblist,
    #     for job in list(joblist):
    #         # task may be expired, refresh() will fail
    #         try:
    #             job.refresh()
    #         except rq.exceptions.NoSuchJobError:
    #             joblist.remove(job)
    #             continue

    #         l.append({
    #             'id': job.get_id(),
    #             'state': job.get_status(),
    #             'progress': job.meta.get('progress'),
    #             'result': job.result
    #         })

    #     return render_template(template_env.get_template("job/index.html"), joblist=l)

    # @app.route('/enqueuejob', methods=['GET', 'POST'])
    # def enqueuejob():
    #     job = jobs.approximate_pi.queue(int(request.form['num_iterations']))
    #     joblist.append(job)
    #     return redirect('/')

    # @app.route('/deletejob', methods=['GET', 'POST'])
    # def deletejob():
    #     if request.args.get('jobid'):
    #         job = rq.job.Job.fetch(request.args.get(
    #             'jobid'), connection=jobs.rq.connection)
    #         job.delete()
    #     return redirect('/')

    return app
