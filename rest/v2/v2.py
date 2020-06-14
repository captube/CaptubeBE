from flask import Blueprint
from flask_restplus import Api

from rest.v2.capture import capture
from rest.v2.archive import archive

blueprint = Blueprint(__name__, '/api/v2', url_prefix='/api/v2')
api = Api(blueprint, title='api', version='2.0')

api.add_namespace(capture, '/capture')
api.add_namespace(archive, '/archive')
