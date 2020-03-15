from core import capture
from core import run


class Capture:
    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        captureItems = self._convertToCaptureItems(
            self._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp))
        self._storeImages(captureItems)
        return captureItems

    def _executeCaptureScript(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        video_info = run.make_youtube_info(url, "", language)
        video_info.save_json()
        capture.capture_by_subs(video_info)
        return video_info

    def _convertToCaptureItems(self, captureItemsByScript):
        convretedItems = {}
        return convretedItems

    def _storeImages(self, captureItems):
        # TODO Call AWS S3 APIs
        return
