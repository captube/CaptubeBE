class Archive:
    def getPagedArchive(self, pageKey, pageSize):
        print(f'getPagedArchive, from : {pageKey} to :{pageSize}')
        # TODO Call AWS S3 APIs with boto
        return {'archives': []}

    def getArchive(self, id):
        print(f'getArchive {id}')
        # TODO Call AWS S3 APIs with boto
        return {'title': '', 'items': [{'url': '', 'startTime': 0, 'endTime': 0, 'subtitle': ''}]}