import json
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
        capture = Capture()
        capture._executeCaptureScript = MagicMock(return_value={})
        capture._convertToCaptureItems = MagicMock(return_value=convertedCaptureItems)
        capture._store = MagicMock(return_value={})

        capture.capture(url, language, numberToCapture, startTimeStamp, endTimeStamp)

        capture._executeCaptureScript.assert_called_with(url, language, numberToCapture, startTimeStamp, endTimeStamp)
        capture._store(convertedCaptureItems)

    def test_executeCaptureScript(self):
        url = "url"
        language = "language"
        numberToCapture = 0
        startTimeStamp = 0
        endTimeStamp = 1
        video_info = MagicMock()
        video_info.save_json = MagicMock(return_value={})
        run.make_youtube_info = MagicMock(return_value=video_info)
        capture.capture_by_subs = MagicMock(return_value={})
        captureBusiness = Capture()

        captureBusiness._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp)

        run.make_youtube_info.assert_called_with(url, "", language)
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
        uuid.uuid4 = MagicMock(return_value=random_uuid)
        capture = Capture()

        convertedCaptureItems = capture._convertToCaptureItems(captureItemsByScript)

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
