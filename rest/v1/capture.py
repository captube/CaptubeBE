from flask_restplus import Namespace, reqparse, Resource

parser = reqparse.RequestParser()

capture = Namespace('capture', description='capture api set')


@capture.route('/')
class GetImages(Resource):
    def post(self):
        parser.add_argument('url', required=True, help='url cannot be null or empty', type=str)
        parser.add_argument('language', required=False, type=str)
        parser.add_argument('numberToCapture', required=False, type=int)
        parser.add_argument('startTimeStamp', required=False, type=int)
        parser.add_argument('endTimeStamp', required=False, type=int)

        args = parser.parse_args()
        print(args)
        # TODO Add core logic to capture

        return '', 200