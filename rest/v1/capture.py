from flask_restplus import Namespace, reqparse, Resource

parser = reqparse.RequestParser()

capture = Namespace('capture', description='capture api set')


@capture.route('/getImages')
class GetImages(Resource):
    def post(self):
        parser.add_argument('url', type=str)
        parser.add_argument('responseEncodingType', type=str)
        parser.add_argument('language', type=str)
        parser.add_argument('isNoSub', type=bool)
        parser.add_argument('numberToCapture', type=int)
        parser.add_argument('startTimeStamp', type=int)
        parser.add_argument('endTimeStamp', type=int)

        args = parser.parse_args()
        print (args)
        # TODO Add core logic to capture

        return '', 200