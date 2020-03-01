from boto3.dynamodb.conditions import Attr

from business import session

dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
archiveTable = dynamodb.Table('archive')
captureItemTable = dynamodb.Table('captureItem')


class Archive:
    def getPagedArchive(self, pageKey, pageSize):
        print(f'getPagedArchive, from : {pageKey} to :{pageSize}')
        # TODO Call AWS S3 APIs with boto
        return {'archives': []}

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