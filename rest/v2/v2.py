from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint(__name__, '/api/v2', url_prefix='/api/v2')
api = Api(blueprint, title='api', version='2.0')
