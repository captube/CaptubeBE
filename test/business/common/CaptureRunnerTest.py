import unittest
from unittest.mock import MagicMock

from business.common.CaptureRunner import CaptureRunner
from core import run, capture


class CaptureRunnerTest(unittest.TestCase):
    def test_capture(self):
        workingDirectory = "workingDirectory"
        url = "url"
        language = "language"
        numberToCapture = "numberToCapture"
        startTimeStamp = "startTimeStamp"
        endTimeStamp = "endTimeStamp"
        captureRunner = CaptureRunner()
        captureRunner._executeCaptureScript = MagicMock(return_value={})

        captureRunner.capture(url, language, numberToCapture, startTimeStamp, endTimeStamp, workingDirectory)

        captureRunner._executeCaptureScript.assert_called_with(url, language, numberToCapture, startTimeStamp,
                                                               endTimeStamp,
                                                               workingDirectory)

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
        captureRunner = CaptureRunner()

        captureRunner._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp, name)

        run.make_youtube_info.assert_called_with(url, name, language)
        video_info.save_json.assert_called_with()
        capture.capture_by_subs.assert_called_with(video_info)
