from flask_restplus import Namespace, Resource, fields, marshal

archive = Namespace('archive', description='archive api set')

archiveItem = archive.model('archive', {
    'id': fields.String,
    'title': fields.String,
    'thumbnailUrl': fields.String,
    'items': fields.String
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


@archive.route('')
class createArchive(Resource):
    parser = archive.parser()

    parser.add_argument('title', required=False, help="Archive title can be null", type=str)
    parser.add_argument('thumbnailUrl', required=False, help="Archive thumbnailUrl can be null", type=str)
    parser.add_argument('archiveItems', required=True, help='captureItems cannot be null or empty', type=str,
                        action='append')

    @archive.expect(parser)
    def post(self):
        args = self.parser.parse_args()
        print(f'archive - incoming args {args}')

        title = args['title']
        thumbnailUrl = args['thumbnailUrl']
        items = args['archiveItems']

        try:
            # TODO Call v2 business logic to create archive
            result = {}
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return 200
