import json
import shutil
import unittest
import uuid
from decimal import Decimal
from unittest.mock import MagicMock

from business.v1.capture import Capture
from core import run, capture


class TestCapture(unittest.TestCase):

    def test_capture(self):
        url = "url"
        language = "language"
        numberToCapture = "numberToCapture"
        startTimeStamp = "startTimeStamp"
        endTimeStamp = "endTimeStamp"
        convertedCaptureItems = []
        random_uuid = 'random_uuid'
        uuid.uuid4 = MagicMock(return_value=random_uuid)
        capture = Capture()
        capture._executeCaptureScript = MagicMock(return_value={})
        capture._convertToCaptureItems = MagicMock(return_value=convertedCaptureItems)
        capture._store = MagicMock(return_value={})
        capture._clearLocalTemporary = MagicMock()

        capture.capture(url, language, numberToCapture, startTimeStamp, endTimeStamp)

        capture._executeCaptureScript.assert_called_with(url, language, numberToCapture, startTimeStamp, endTimeStamp,
                                                         random_uuid)
        capture._store.assert_called_with(convertedCaptureItems)
        capture._clearLocalTemporary.assert_called_with(random_uuid)

    def test_executeCaptureScript(self):
        url = "url"
        language = "language"
        name = "name"
        numberToCapture = 0
        startTimeStamp = 0
        endTimeStamp = 1
        video_info = MagicMock()
        video_info.save_json = MagicMock(return_value={})
        run.make_youtube_info = MagicMock(return_value=video_info)
        capture.capture_by_subs = MagicMock(return_value={})
        captureBusiness = Capture()

        captureBusiness._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp, name)

        run.make_youtube_info.assert_called_with(url, name, language)
        video_info.save_json.assert_called_with()
        capture.capture_by_subs.assert_called_with(video_info)

    def test_convertToCaptureItems(self):
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        captureItemsByScript = {
            "title": title,
            "thumbnail": thumbnailUrl,
            "frame_infos": [{
                "frame_num": 0,
                "time_info": 3.5,
                "script": "script1",
                "img_path": "img_path1"},
                {
                    "frame_num": 1,
                    "time_info": 4.5,
                    "script": "script2",
                    "img_path": "img_path2"}
                ,
                {
                    "frame_num": 2,
                    "time_info": 5.5,
                    "script": "script2",
                    "img_path": "img_path2"}
            ]
        }
        random_uuid = 'random_uuid'
        capture = Capture()

        convertedCaptureItems = capture._convertToCaptureItems(captureItemsByScript, random_uuid)

        self.assertEqual(captureItemsByScript["title"], convertedCaptureItems["title"])
        self.assertEqual(random_uuid, convertedCaptureItems["id"])
        self.assertEqual(thumbnailUrl, convertedCaptureItems["thumbnailUrl"])
        self.assertEqual(captureItemsByScript["frame_infos"][0]["img_path"],
                         convertedCaptureItems["captureItems"][0]["url"])
        self.assertEqual(captureItemsByScript["frame_infos"][0]["script"],
                         convertedCaptureItems["captureItems"][0]["subtitle"])
        self.assertEqual(captureItemsByScript["frame_infos"][0]["time_info"],
                         convertedCaptureItems["captureItems"][0]["startTime"])
        self.assertEqual(captureItemsByScript["frame_infos"][0]["time_info"],
                         convertedCaptureItems["captureItems"][0]["endTime"])
        self.assertEqual(f'{random_uuid}_{captureItemsByScript["frame_infos"][0]["frame_num"]}',
                         convertedCaptureItems["captureItems"][0]["id"])
        self.assertEqual(captureItemsByScript["frame_infos"][1]["img_path"],
                         convertedCaptureItems["captureItems"][1]["url"])
        self.assertEqual(captureItemsByScript["frame_infos"][1]["script"],
                         convertedCaptureItems["captureItems"][1]["subtitle"])
        self.assertEqual(captureItemsByScript["frame_infos"][1]["time_info"],
                         convertedCaptureItems["captureItems"][1]["startTime"])
        self.assertEqual(captureItemsByScript["frame_infos"][1]["time_info"],
                         convertedCaptureItems["captureItems"][1]["endTime"])
        self.assertEqual(f'{random_uuid}_{captureItemsByScript["frame_infos"][1]["frame_num"]}',
                         convertedCaptureItems["captureItems"][1]["id"])
        self.assertEqual(captureItemsByScript["frame_infos"][2]["img_path"],
                         convertedCaptureItems["captureItems"][2]["url"])
        self.assertEqual(captureItemsByScript["frame_infos"][2]["script"],
                         convertedCaptureItems["captureItems"][2]["subtitle"])
        self.assertEqual(captureItemsByScript["frame_infos"][2]["time_info"],
                         convertedCaptureItems["captureItems"][2]["startTime"])
        self.assertEqual(captureItemsByScript["frame_infos"][2]["time_info"],
                         convertedCaptureItems["captureItems"][2]["endTime"])
        self.assertEqual(f'{random_uuid}_{captureItemsByScript["frame_infos"][2]["frame_num"]}',
                         convertedCaptureItems["captureItems"][2]["id"])

    def test_store(self):
        convertedCaptureItems = []
        urlAdjustedCaptureItems = []
        capture = Capture()
        capture._storeImages = MagicMock(return_value=urlAdjustedCaptureItems)
        capture._storeMetadata = MagicMock(return_value={})

        capture._store(convertedCaptureItems)

        capture._storeImages.assert_called_with(convertedCaptureItems)
        capture._storeMetadata.assert_called_with(urlAdjustedCaptureItems)

    def test__storeMetadata(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "startTime": "startTime1",
                         "endTime": "endTime1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "startTime": "startTime2",
                         "endTime": "endTime2",
                         "subtitle": "subtitle2",
                         "url": "url2"}]
        urlAdjustedItems = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        capture = Capture()
        Capture.archiveTable = MagicMock()
        Capture.archiveTable.put_item = MagicMock(return_value={})
        Capture.captureItemTable = MagicMock()
        Capture.captureItemTable.put_item = MagicMock(return_value={})

        capture._storeMetadata(urlAdjustedItems)

        Capture.archiveTable.put_item.assert_called_with(Item={
            'id': urlAdjustedItems['id'],
            'title': urlAdjustedItems['title'],
            'thumbnailUrl': urlAdjustedItems['thumbnailUrl']
        })
        # FIXME Cannot record previous call
        # Capture.captureItemTable.put_item.assert_called_with(Item={
        #     "id": urlAdjustedItems['captureItems'][0]["id"],
        #     "archiveId": urlAdjustedItems["id"],
        #     "startTime": urlAdjustedItems['captureItems'][0]["startTime"],
        #     "endTime": urlAdjustedItems['captureItems'][0]["endTime"],
        #     "subtitle": urlAdjustedItems['captureItems'][0]["subtitle"],
        #     "url": urlAdjustedItems['captureItems'][0]["url"]
        # })
        Capture.captureItemTable.put_item.assert_called_with(Item=json.loads(json.dumps({
            "id": urlAdjustedItems['captureItems'][1]["id"],
            "archiveId": urlAdjustedItems["id"],
            "startTime": urlAdjustedItems['captureItems'][1]["startTime"],
            "endTime": urlAdjustedItems['captureItems'][1]["endTime"],
            "subtitle": urlAdjustedItems['captureItems'][1]["subtitle"],
            "url": urlAdjustedItems['captureItems'][1]["url"]
        }), parse_float=Decimal))

    def test__convertAsS3Url(self):
        fileName = "MieyJ34_01.png"
        capture = Capture()

        convertedPath = capture._convertAsS3Url(fileName)

        self.assertEqual(f'{capture.S3_PREFIX}{fileName}', convertedPath)

    def test__storeImages(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        fileName1 = "MieyJ34_01.png"
        url1 = f"/home/captube/MieyJ34/imgs/{fileName1}"
        fileName2 = "MieyJ34_02.png"
        url2 = f"/home/captube/MieyJ34/imgs/{fileName2}"

        captureItems = [{"id": "id1",
                         "startTime": "startTime1",
                         "endTime": "endTime1",
                         "subtitle": "subtitle1",
                         "url": url1},
                        {"id": "id2",
                         "startTime": "startTime2",
                         "endTime": "endTime2",
                         "subtitle": "subtitle2",
                         "url": url2}]
        convertedItems = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        capture = Capture()
        Capture.s3_client = MagicMock()
        Capture.s3_client.upload_file = MagicMock()

        adjustedItems = capture._storeImages(convertedItems)

        self.assertEqual(f'{capture.S3_PREFIX}{fileName1}', adjustedItems['captureItems'][0]['url'])
        self.assertEqual(f'{capture.S3_PREFIX}{fileName2}', adjustedItems['captureItems'][1]['url'])
        # FIXME Cannot record previous call
        # Capture.s3_client.upload_file.assert_called_with(url1, capture.S3_BUCKET, fileName1, ExtraArgs={
        #                     'ContentType': 'image/jpeg'
        #                 })
        Capture.s3_client.upload_file.assert_called_with(url2, capture.S3_BUCKET, fileName2, ExtraArgs={
            'ContentType': 'image/jpeg'
        })

    def test__clearLocalTemporary(self):
        capture = Capture()
        id = "id"
        shutil.rmtree = MagicMock()

        capture._clearLocalTemporary(id)

        shutil.rmtree.assert_called_with(f'{capture.RESULT_DIR}/{id}')

    def test_capture_call__clearLocalTemporary_when_exception(self):
        capture = Capture()
        capture._executeCaptureScript = MagicMock()
        capture._executeCaptureScript.side_effect = Exception("")
        capture._clearLocalTemporary = MagicMock()
        random_uuid = 'random_uuid'
        uuid.uuid4 = MagicMock(return_value=random_uuid)

        try:
            capture.capture("url", "language", 0, 1, 2)
        except Exception as e:
            print(e)

        capture._clearLocalTemporary.assert_called_with(random_uuid)
