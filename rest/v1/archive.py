import ast

from flask_restplus import Namespace, reqparse, Resource, fields, marshal

from business.v1.archive import Archive

parser = reqparse.RequestParser()
archive = Namespace('archive', description='archive api set')


@archive.route('/list')
class getArchiveList(Resource):
    PAGE_KEY = 'pageKey'
    PAGE_SIZE = 'pageSize'

    def get(self):
        parser.add_argument(self.PAGE_KEY, required=False, type=str, location='args')
        parser.add_argument(self.PAGE_SIZE, required=False, type=str, location='args')

        args = parser.parse_args()
        print(f'archive/list - incoming args {args}')

        try:
            # TODO : Need DI for Archive, not creating dynamically
            result = Archive().getPagedArchive(
                ast.literal_eval(args[self.PAGE_KEY]) if args[self.PAGE_KEY] is not None else None
                , args[self.PAGE_SIZE])
        except Exception as e:
            print(f'Exception occured during getPagedArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, multiArchiveMetadata), 200


singleArchiveMetadata = archive.model('singleArchiveMetadata', {
    'id': fields.String,
    'thumbnailUrl': fields.String,
    'title': fields.String
})

multiArchiveMetadata = archive.model('multiArchiveMetadata', {
    'nextPageKey': fields.Wildcard(fields.String),
    'archives': fields.List(fields.Nested(singleArchiveMetadata))
})


@archive.route('/<string:id>')
class getArchive(Resource):

    def get(self, id):
        print(f'archive item - id {id}')

        try:
            # TODO : Need DI for Archive, not creating dynamically
            result = Archive().getArchive(id)
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveItem), 200


captureItem = archive.model('captureItem', {
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
