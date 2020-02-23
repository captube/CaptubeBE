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
        return marshal(result, archiveResult), 200

    def getPagedArchive(self, pageFrom, pageTo):
        print(f'getPagedArchive, from : {pageFrom} to :{pageTo}')


archiveItem = archive.model('archiveItem', {
    'url': fields.String,
    'startTime': fields.Integer,
    'endTime': fields.Integer,
    'subtitle': fields.String
})

archiveResult = archive.model('archive', {
    'title': fields.String,
    'items': fields.Nested(archiveItem)
})
