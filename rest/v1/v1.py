from flask import Blueprint
from flask_restplus import Api

from rest.v1.capture import capture
from rest.v1.archive import archive

blueprint = Blueprint(__name__, '/api/v1', url_prefix='/api/v1')
api = Api(blueprint, title='api', version='1.0')

api.add_namespace(capture, '/capture')
api.add_namespace(archive, '/archive')