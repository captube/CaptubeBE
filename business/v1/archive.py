from boto3.dynamodb.conditions import Attr

from business import session

dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
archiveTable = dynamodb.Table('archive')
captureItemTable = dynamodb.Table('captureItem')


class Archive:
    _DEFAULT_PAGE_SIZE = 25

    def getPagedArchive(self, pageKey, pageSize):
        print(f'getPagedArchive, pageKey : {pageKey} pageSize :{pageSize}')
        limit = self._DEFAULT_PAGE_SIZE if pageSize is None else pageSize
        if pageKey is None:
            print(f'getPagedArchive - query only with limit {limit}')
            queryResult = archiveTable.scan(Limit=int(limit))
        else:
            print(f'getPagedArchive - query with limit {limit} and ExclusiveStartKey {pageKey}')
            queryResult = archiveTable.scan(
                Limit=int(limit),
                ExclusiveStartKey=pageKey)

        print(f'paged archives from dynamo : {queryResult}')

        response = {'archives': queryResult['Items'], 'nextPageKey': queryResult['LastEvaluatedKey']} \
            if 'LastEvaluatedKey' in queryResult else \
            {'archives': queryResult['Items']}

        return response

    def getArchive(self, id):
        print(f'getArchive {id}')
        response = archiveTable.get_item(Key={
            'id': id
        })

        archive = archiveTable.get_item(Key={
            'id': id
        })['Item']
        print(f'archive from dynamo : {archive}')
        captureItems = captureItemTable.scan(
            FilterExpression=Attr('archiveId').eq(archive['id'])
        )['Items']
        print(f'captureItems from dynamo : {len(captureItems)}')

        response = {
            'title': archive['title'],
            'items': captureItems
        }
        print(f'getArchive response : {response}')

        return response
