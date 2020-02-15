from flask import Flask
from flask_restplus import Api

from rest.v1.v1 import blueprint as api

flask_app = Flask(__name__)
flask_app.register_blueprint(api)

if __name__ == '__main__':
    flask_app.run()