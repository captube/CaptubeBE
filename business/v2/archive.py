from business import session


class Archive:
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    editableArchiveTable = dynamodb.Table('editableArchive')
    captionTable = dynamodb.Table('caption')

    def getArchive(self, id):
        print(f'getArchive {id}')

        archive = self.editableArchiveTable.get_item(Key={
            'id': id
        })['Item']
        captionIds = sorted(archive['items'])
        captions = []
        archive['items'] = []

        # TODO : Need to optimize by requesting with list
        for captionId in captionIds:
            captions.append(self.captionTable.get_item(Key={
                'id': captionId
            })['Item'])

        archive['items'] = captions

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
