import json
from decimal import Decimal

from boto3.dynamodb.conditions import Attr

from business import session


class CaptureSaver:
    S3_BUCKET = "captube.captures"
    S3_PREFIX = "https://s3.ap-northeast-2.amazonaws.com/captube.captures/"
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    videoTable = dynamodb.Table('video')
    captionTable = dynamodb.Table('caption')

    s3_client = session.client('s3')

    def save(self, captureInformation):
        print(f'save, {captureInformation}')
        self._storeVideoMetadata(captureInformation)
        self._storeImages(captureInformation)
        return

    def _storeImages(self, captureInformation):
        try:
            toSaveCaptures = self._getToSaveCaptures(captureInformation)

            for captureItem in toSaveCaptures:
                self.s3_client.upload_file(captureItem['localFilePath'], self.S3_BUCKET, captureItem['saveFileName'],
                                           ExtraArgs={
                                               'ContentType': 'image/jpeg'
                                           })
                self.s3_client.upload_file(captureItem['localNoSubtitleFilePath'], self.S3_BUCKET, captureItem['noSubtitleSaveFileName'],
                                           ExtraArgs={
                                               'ContentType': 'image/jpeg'
                                           })

                response = self.captionTable.put_item(
                    Item=json.loads(json.dumps({
                        "id": captureItem["id"],
                        "videoId": captureInformation["id"],
                        "timeStamp": captureItem["timeStamp"],
                        "subtitle": captureItem["subtitle"],
                        "url": captureItem["url"],
                        "noSubtitleUrl": captureItem["noSubtitleUrl"]
                    }), parse_float=Decimal))

                print(f'Succeed to store captureItem {captureItem["id"]}')
                print(json.dumps(response, indent=4))

        except Exception as e:
            # TODO : Need exception handling logic, such as removing failed item.
            raise e

    def _getToSaveCaptures(self, captureInformation):
        result = []
        videoId = captureInformation['id']
        capturedItems = captureInformation['captureItems']
        startTime = capturedItems[0]['timeStamp']
        endTime = capturedItems[-1]['timeStamp']
        if startTime > endTime:
            return result

        storedCaptions = self._getCaptions(videoId, startTime, endTime)

        for captureItem in capturedItems:
            exist = False
            for storedCaption in storedCaptions:
                if captureItem['id'] == storedCaption['id']:
                    exist = True
                    break

            if not exist:
                result.append(captureItem)

        return result

    def _getCaptions(self, videoId, startTime, endTime):
        captions = self.captionTable.scan(
            FilterExpression=Attr('videoId').eq(videoId) & Attr('timeStamp').gte(Decimal(startTime)) & Attr(
                'timeStamp').lte(
                Decimal(endTime)))['Items']
        print(f'captions from dynamo : {len(captions)} for {videoId} between {startTime} and {endTime}')

        return captions

    def _storeVideoMetadata(self, captureInformation):
        try:
            if self._needSaveVideoMetadata(captureInformation['id']):
                response = self.videoTable.put_item(
                    Item={
                        'id': captureInformation['id'],
                        'title': captureInformation['title'],
                        'thumbnailUrl': captureInformation['thumbnailUrl']
                    })

                print(f'Succeed to store Archive {captureInformation["id"]}')
                print(json.dumps(response, indent=4))
        except Exception as e:
            # TODO : Need exception handling logic, such as removing failed item.
            raise e

    def _needSaveVideoMetadata(self, id):
        return self._getVideo(id) == None

    def _getVideo(self, id):
        response = self.videoTable.get_item(Key={'id': id})
        video = None
        if 'Item' in response:
            video = response['Item']

        print(f'video from dynamo : {video} for {id}')

        return video
