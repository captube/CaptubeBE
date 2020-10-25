import unittest
import uuid
from unittest.mock import MagicMock

from business.v2.capture import Capture


class TestCapture(unittest.TestCase):
    def test_getLanguage(self):
        # TODO : Cannot test getLanguage, because core.youtube.youtube requires paremeter which is not business logic
        # capture = Capture()
        # url = "someUrl"
        # mockCaption = {}
        # mockLanguages = []
        # core.youtube.youtube = MagicMock(return_value={
        #     'get_captions' :  MagicMock(return_value=mockCaption),
        #     'get_available_langs' : MagicMock(return_value=mockLanguages)
        # })
        # capture._youtube = core.youtube.youtube(url)
        #
        # result = capture.getAvailableLanguage(url)
        #
        # capture._youtube.get_captions.assert_called_with(url)
        # capture._youtube.get_available_langs.assert_called_with(mockCaption)
        # self.assertEqual(url, result)
        return

    def test_capture(self):
        videoId = "videoId"
        url = "url"
        language = "language"
        numberToCapture = None
        startTimerStamp = None
        endTimeStamp = None
        woringPath = "woringPath"
        uuid.uuid4 = MagicMock(return_value=woringPath)
        capture = Capture()
        capture.youtubeIdParser.parse = MagicMock(return_value=videoId)
        capture._clearLocalTemporary = MagicMock(return_value={})
        videoInformation = {}
        capture.captureRunner.capture = MagicMock(return_value=videoInformation)
        captureInformation = {}
        capture._asCaptureInformation = MagicMock(return_value=captureInformation)
        capture.captureSaver.save = MagicMock()

        capture.capture(url, language, numberToCapture, startTimerStamp, endTimeStamp)

        capture.captureRunner.capture.assert_called_with(url, language, numberToCapture, startTimerStamp, endTimeStamp,
                                                         woringPath)
        capture._asCaptureInformation.assert_called_with(videoInformation, f'{videoId}_{language}')
        capture.captureSaver.save.assert_called_with(captureInformation)
        capture._clearLocalTemporary.assert_called()

    def test_capture_when_exception(self):
        videoId = "videoId"
        url = "url"
        language = "language"
        numberToCapture = None
        startTimerStamp = None
        endTimeStamp = None
        woringPath = "woringPath"
        uuid.uuid4 = MagicMock(return_value=woringPath)
        capture = Capture()
        capture.youtubeIdParser.parse = MagicMock(return_value=videoId)
        capture._clearLocalTemporary = MagicMock(return_value={})
        videoInformation = {}
        capture.captureRunner.capture = MagicMock(return_value=videoInformation)
        captureInformation = {}
        capture._asCaptureInformation = MagicMock(return_value=captureInformation)
        capture.captureSaver.save = MagicMock()

        capture.capture(url, language, numberToCapture, startTimerStamp, endTimeStamp)

        capture.captureRunner.capture.assert_called_with(url, language, numberToCapture, startTimerStamp, endTimeStamp,
                                                         woringPath)
        capture._asCaptureInformation.assert_called_with(videoInformation, f'{videoId}_{language}')
        capture.captureSaver.save.assert_called_with(captureInformation)
        capture._clearLocalTemporary.assert_called()

    def test__convertAsS3Url(self):
        fileName = "MieyJ34_01.png"
        capture = Capture()

        convertedPath = capture._convertAsS3Url(fileName)

        self.assertEqual(f'{capture.S3_PREFIX}{fileName}', convertedPath)

    def test__asCaptureInformation(self):
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        id = "id"
        frameInformation = [{
            "frame_num": 0,
            "img_path": "/home/captube/result/0.jpg",
            "script": "script0"
        }, {
            "frame_num": 1,
            "img_path": "/home/captube/result/1.jpg",
            "script": "script1"
        }, {
            "frame_num": 2,
            "img_path": "/home/captube/result/2.jpg",
            "script": "script2"
        }, {
            "frame_num": 3,
            "img_path": "/home/captube/result/3.jpg",
            "script": "script3"
        }, {
            "frame_num": 4,
            "img_path": "/home/captube/result/4.jpg",
            "script": "script4"
        }]

        captureResultByScript = {
            "title": title,
            "thumbnail": thumbnailUrl,
            "frame_infos": frameInformation
        }

        capture = Capture()
        result = capture._asCaptureInformation(captureResultByScript, id)

        expected = {
            "title": title,
            "thumbnailUrl": thumbnailUrl,
            "id": id,
            "captureItems": [
                {"id": "id_0",
                 "frameNumber": 0,
                 "url": capture._convertAsS3Url("id_0.jpg"),
                 "localFilePath": frameInformation[0]["img_path"],
                 "saveFileName": "id_0.jpg",
                 "timeStamp": 0,
                 "subtitle": frameInformation[0]["script"]
                 },
                {"id": "id_1",
                 "frameNumber": 1,
                 "url": capture._convertAsS3Url("id_1.jpg"),
                 "localFilePath": frameInformation[1]["img_path"],
                 "saveFileName": "id_1.jpg",
                 "timeStamp": 0,
                 "subtitle": frameInformation[1]["script"]
                 },
                {"id": "id_2",
                 "frameNumber": 2,
                 "url": capture._convertAsS3Url("id_2.jpg"),
                 "localFilePath": frameInformation[2]["img_path"],
                 "saveFileName": "id_2.jpg",
                 "timeStamp": 0,
                 "subtitle": frameInformation[2]["script"]
                 },
                {"id": "id_3",
                 "frameNumber": 3,
                 "url": capture._convertAsS3Url("id_3.jpg"),
                 "localFilePath": frameInformation[3]["img_path"],
                 "saveFileName": "id_3.jpg",
                 "timeStamp": 0,
                 "subtitle": frameInformation[3]["script"]
                 },
                {"id": "id_4",
                 "frameNumber": 4,
                 "url": capture._convertAsS3Url("id_4.jpg"),
                 "localFilePath": frameInformation[4]["img_path"],
                 "saveFileName": "id_4.jpg",
                 "timeStamp": 0,
                 "subtitle": frameInformation[4]["script"]
                 }
            ]
        }

        self.assertEqual(expected, result)
