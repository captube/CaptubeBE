from flask import Flask

from rest.v1.v1 import blueprint as v1api
from rest.v2.v2 import blueprint as v2api

flask_app = Flask(__name__)
flask_app.register_blueprint(v1api)
flask_app.register_blueprint(v2api)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0')
