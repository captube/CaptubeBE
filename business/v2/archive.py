from business import session


class Archive:
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    editableArchiveTable = dynamodb.Table('editableArchive')

    def getArchive(self, id):
        print(f'getArchive {id}')

        archive = self.editableArchiveTable.get_item(Key={
            'id': id
        })['Item']
        print(f'archive from dynamo : {archive}')

        return archive

    def setArchive(self, id, title, thumbnailUrl, items):
        print(f'setArchive {id} {title} {thumbnailUrl} {items}')

        self.editableArchiveTable.put_item(
            Item={
                'id': id,
                'title': title,
                'thumbnailUrl': thumbnailUrl,
                'items': items
            })

        return {'id': id}
