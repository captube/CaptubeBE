from flask_restplus import Namespace, reqparse, Resource, fields, marshal

parser = reqparse.RequestParser()
archive = Namespace('archive', description='archive api set')


@archive.route('/list')
class getArchiveList(Resource):
    PAGE_FROM = 'pageFrom'
    PAGE_TO = 'pageTo'

    def get(self):
        parser.add_argument(self.PAGE_FROM, required=True, type=str, location='args')
        parser.add_argument(self.PAGE_TO, required=True, type=str, location='args')

        args = parser.parse_args()
        print(f'archive/list - incoming args {args}')

        try:
            result = self.getPagedArchive(args[self.PAGE_FROM], args[self.PAGE_TO])
        except Exception as e:
            print(f'Exception occured during getPagedArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, multiArchiveMetadata), 200

    def getPagedArchive(self, pageFrom, pageTo):
        print(f'getPagedArchive, from : {pageFrom} to :{pageTo}')
        return {'archives': []}


singleArchiveMetadata = archive.model('singleArchiveMetadata', {
    'id': fields.String,
    'title': fields.String
})

multiArchiveMetadata = archive.model('multiArchiveMetadata', {
    'archives': fields.List(fields.Nested(singleArchiveMetadata))
})


@archive.route('/<string:id>')
class getArchive(Resource):

    def get(self, id):
        print(f'archive item - id {id}')

        try:
            result = self.getArchive(id)
        except Exception as e:
            print(f'Exception occured during getArchive {e}')
            return 'Internal Server Error', 500
        return marshal(result, archiveItem), 200

    def getArchive(self, id):
        print(f'getArchive {id}')
        return {'title': '', 'items': [{'url': '', 'startTime': 0, 'endTime': 0, 'subtitle': ''}]}


captureItem = archive.model('captureItem', {
    'url': fields.String,
    'startTime': fields.Integer,
    'endTime': fields.Integer,
    'subtitle': fields.String
})

archiveItem = archive.model('archive', {
    'title': fields.String,
    'items': fields.Nested(captureItem)
})