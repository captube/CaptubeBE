from flask_restplus import Namespace, reqparse, Resource, marshal, fields

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
        print(f'capture - incoming args {args}')

        try:
            result = self.capture(args)
        except Exception as e:
            print(f'Exception occured during capture {e}')
            return 'Internal Server Error', 500
        return marshal(result, captureResult), 200

    def capture(self, args):
        result = {}
        # TODO Add core logic to capture
        return result


captureItem = capture.model('captureItems', {
    'url': fields.String,
    'startTime': fields.Integer,
    'endTime': fields.Integer,
    'subtitle': fields.String
})

captureResult = capture.model('CaptureResult', {
    'id': fields.String,
    'title': fields.String,
    'captureItems': fields.List(fields.Nested(captureItem))
})