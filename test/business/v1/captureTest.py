import unittest
from unittest.mock import MagicMock

from business.v1.capture import Capture


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