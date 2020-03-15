import json
import os
import uuid
from decimal import Decimal

from business import session
from core import capture
from core import run


class Capture:
    S3_BUCKET = "captube.captures"
    S3_PREFIX = "https://s3.ap-northeast-2.amazonaws.com/captube.captures/"
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    archiveTable = dynamodb.Table('archive')
    captureItemTable = dynamodb.Table('captureItem')

    s3_client = session.client('s3')

    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        print(f'capture, {url}, {language}, {numberToCapture}, {startTimeStamp}, {endTimeStamp}')
        id = str(uuid.uuid4())
        video_info = self._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp, id)
        captureItems = self._convertToCaptureItems(video_info, id)
        self._store(captureItems)
        return captureItems

    def _executeCaptureScript(self, url, language, numberToCapture, startTimeStamp, endTimeStamp, name):
        print(f'execute capture script, {url}, {language}, {numberToCapture}, {startTimeStamp}, {endTimeStamp}, {name}')
        video_info = run.make_youtube_info(url, name, language)
        video_info.save_json()
        capture.capture_by_subs(video_info)
        print(f'video_info : {video_info}')
        return video_info

    def _convertToCaptureItems(self, captureItemsByScript, id):
        convretedItems = {
            "title": captureItemsByScript["title"],
            "thumbnailUrl": captureItemsByScript["thumbnail"],
            "id": id,
            "captureItems": []
        }

        frame_infos = captureItemsByScript["frame_infos"]
        for frame_info in frame_infos:
            convretedItems["captureItems"].append({
                "id": f'{convretedItems["id"]}_{frame_info["frame_num"]}',
                "url": frame_info["img_path"],
                "startTime": frame_info["time_info"],
                "endTime": frame_info["time_info"],
                "subtitle": frame_info["script"]
            })

        return convretedItems

    def _store(self, convertedItems):
        print(f'store, {convertedItems}')
        urlAdjustedItems = self._storeImages(convertedItems)
        self._storeMetadata(urlAdjustedItems)
        return

    def _storeImages(self, convertedItems):
        try:
            for captureItem in convertedItems["captureItems"]:
                captureFilePath = captureItem["url"]
                captureFileName = os.path.basename(captureItem["url"])
                captureItem["url"] = self._convertAsS3Url(captureFileName)
                self.s3_client.upload_file(captureFilePath, self.S3_BUCKET, captureFileName, ExtraArgs={
                    'ContentType': 'image/jpeg'
                })
        except Exception as e:
            # TODO : Need exception handling logic, such as removing failed item.
            raise e

        return convertedItems

    def _convertAsS3Url(self, fileName):
        return f'{self.S3_PREFIX}{fileName}'

    def _storeMetadata(self, urlAdjustedItems):
        try:
            response = self.archiveTable.put_item(
                Item={
                    'id': urlAdjustedItems['id'],
                    'title': urlAdjustedItems['title'],
                    'thumbnailUrl': urlAdjustedItems['thumbnailUrl']
                })

            print(f'Succeed to store Archive {urlAdjustedItems["id"]}')
            print(json.dumps(response, indent=4))

            for captureItem in urlAdjustedItems["captureItems"]:
                response = self.captureItemTable.put_item(
                    Item=json.loads(json.dumps({
                        "id": captureItem["id"],
                        "archiveId": urlAdjustedItems["id"],
                        "startTime": captureItem["startTime"],
                        "endTime": captureItem["endTime"],
                        "subtitle": captureItem["subtitle"],
                        "url": captureItem["url"]
                    }), parse_float=Decimal))

                print(f'Succeed to store captureItem {captureItem["id"]}')
                print(json.dumps(response, indent=4))

        except Exception as e:
            # TODO : Need exception handling logic, such as removing failed item.
            raise e

        return
