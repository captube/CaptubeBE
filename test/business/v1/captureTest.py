import unittest
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
        capture = Capture()
        capture._executeCaptureScript = MagicMock(return_value={})

        capture.capture(url, language, numberToCapture, startTimeStamp, endTimeStamp)

        capture._executeCaptureScript.assert_called_with(url, language, numberToCapture, startTimeStamp, endTimeStamp)

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
