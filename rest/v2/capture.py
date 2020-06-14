import sys
import traceback

from flask_restplus import Namespace, Resource, marshal, fields

capture = Namespace('capture', description='capture api set')

captureParams = capture.model('CaptureParams', {
    'url': fields.String(required=True),
    'language': fields.String(required=False),
    'numberToCapture': fields.Integer(min=0, required=False),
    'startTimeStamp': fields.Integer(min=0, required=False),
    'endTimeStamp': fields.Integer(min=0, required=False)
})

captureItem = capture.model('captureItems', {
    'id': fields.String,
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


@capture.route('')
class GetImages(Resource):
    parser = capture.parser()

    parser.add_argument('url', required=True, help='url cannot be null or empty', type=str)
    parser.add_argument('language', required=False, type=str, default="en")
    parser.add_argument('numberToCapture', required=False, type=int)
    parser.add_argument('startTimeStamp', required=False, type=int)
    parser.add_argument('endTimeStamp', required=False, type=int)

    @capture.expect(captureParams)
    def post(self):

        args = self.parser.parse_args()
        print(f'capture - incoming args {args}')

        try:
            url = args['url']
            language = args['language']
            numberToCapture = args['numberToCapture']
            startTimeStamp = args['startTimeStamp']
            endTimeStamp = args['endTimeStamp']
            # TODO Call v2 business logic for capture
            result = {}
        except Exception as e:
            print(f'Exception occured during capture {e}')
            traceback.print_exc(file=sys.stdout)
            return 'Internal Server Error', 500
        return marshal(result, captureResult), 200


languageResult = capture.model('languageResult', {
    'languages': fields.List(fields.String)
})


@capture.route('/language')
class GetAvailableLanguage(Resource):
    parser = capture.parser()

    parser.add_argument('url', required=True, help='url cannot be null or empty', type=str)

    @capture.expect(parser)
    def get(self):

        args = self.parser.parse_args()
        print(f'Get available language - incoming args {args}')

        try:
            url = args['url']
            # TODO Call v2 business logic to get available language
            result = {}
        except Exception as e:
            print(f'Exception occured during capture {e}')
            traceback.print_exc(file=sys.stdout)
            return 'Internal Server Error', 500
        return marshal(result, languageResult), 200
