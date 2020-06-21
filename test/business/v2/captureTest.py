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
