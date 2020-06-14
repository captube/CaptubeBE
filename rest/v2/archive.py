from flask_restplus import Namespace, Resource, fields, marshal

archive = Namespace('archive', description='archive api set')

captureItem = archive.model('captureItem', {
    'id': fields.String,
    'url': fields.String,
    'startTime': fields.Integer,
    'endTime': fields.Integer,
    'subtitle': fields.String
})

archiveItem = archive.model('archive', {
    'title': fields.String,
    'thumbnailUrl': fields.String,
    'items': fields.Nested(captureItem)
})


@archive.route('/<string:id>')
class getArchive(Resource):

    def get(self, id):
        print(f'archive item - id {id}')

        try:
            # TODO Call v2 business logic to get archive
            result = {}
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveItem), 200


captureItem = archive.model('captureItem', {
    'id': fields.String,
    'url': fields.String,
    'startTime': fields.Integer,
    'endTime': fields.Integer,
    'subtitle': fields.String
})

archiveItem = archive.model('archive', {
    'id': fields.String,
    'title': fields.String,
    'thumbnailUrl': fields.String,
    'items': fields.Nested(captureItem)
})


@archive.route('')
class createArchive(Resource):
    parser = archive.parser()

    parser.add_argument('archiveItems', required=True, help='captureItems cannot be null or empty', type=str,
                        action='append')

    @archive.expect(parser)
    def post(self):
        args = self.parser.parse_args()
        print(f'archive - incoming args {args}')

        try:
            # TODO Call v2 business logic to create archive
            result = {}
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveItem), 200
