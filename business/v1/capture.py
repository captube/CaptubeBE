import json
import uuid
from decimal import Decimal

from business import session
from core import capture
from core import run


class Capture:
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    archiveTable = dynamodb.Table('archive')
    captureItemTable = dynamodb.Table('captureItem')

    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        captureItems = self._convertToCaptureItems(
            self._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp))
        self._store(captureItems)
        return captureItems

    def _executeCaptureScript(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        video_info = run.make_youtube_info(url, "", language)
        video_info.save_json()
        capture.capture_by_subs(video_info)
        return video_info

    def _convertToCaptureItems(self, captureItemsByScript):
        convretedItems = {
            "title": captureItemsByScript["title"],
            "thumbnailUrl": captureItemsByScript["thumbnail"],
            "id": uuid.uuid4(),
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
        urlAdjustedItems = self._storeImages(convertedItems)
        self._storeMetadata(urlAdjustedItems)
        return

    def _storeImages(self, convertedItems):
        return

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
