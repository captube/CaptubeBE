from flask import Blueprint
from flask_restplus import Api

from rest.v2.capture import capture

blueprint = Blueprint(__name__, '/api/v2', url_prefix='/api/v2')
api = Api(blueprint, title='api', version='2.0')

api.add_namespace(capture, '/capture')
