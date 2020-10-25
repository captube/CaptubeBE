import uuid

from flask_restplus import Namespace, Resource, fields, marshal

from business.v2.archive import Archive

archive = Namespace('archive', description='archive api set')

captureItem = archive.model('captureItem', {
    'id': fields.String,
    'url': fields.String,
    'timestamp': fields.Integer,
    'subtitle': fields.String,
    'videoId': fields.String
})

archiveItem = archive.model('archive', {
    'id': fields.String,
    'title': fields.String,
    'thumbnailUrl': fields.String,
    'items': fields.List(fields.Nested(captureItem))
})


@archive.route('/<string:id>')
class getArchive(Resource):

    def get(self, id):
        print(f'archive item - id {id}')

        try:
            # TODO Archive need to be DI not Object creation
            result = Archive().getArchive(id)
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveItem), 200


archiveResult = archive.model('archiveResult', {
    'id': fields.String
})

requestCreateArchive = archive.model('RequestCreateArchive', {
    'title': fields.String(required=False),
    'thumbnailUrl': fields.String(required=False),
    'archiveItems': fields.List(fields.String, required=True)
})

@archive.route('')
class createArchive(Resource):
    parser = archive.parser()

    parser.add_argument('title', required=False, help="Archive title can be null", type=str)
    parser.add_argument('thumbnailUrl', required=False, help="Archive thumbnailUrl can be null", type=str)
    parser.add_argument('archiveItems', required=True, help='ArchiveItems cannot be null or empty', action='append')

    @archive.expect(requestCreateArchive)
    def post(self):
        args = self.parser.parse_args()
        print(f'archive - incoming args {args}')

        title = args['title']
        thumbnailUrl = args['thumbnailUrl']
        items = args['archiveItems']

        try:
            # TODO Archive need to be DI not Object creation
            result = Archive().setArchive(str(uuid.uuid4()), title, thumbnailUrl, items)
        except Exception as e:
            print(f'Exception occured during setArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveResult), 200
