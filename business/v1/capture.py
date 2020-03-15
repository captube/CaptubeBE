import uuid

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

    def _storeImages(self, captureItems):
        # TODO Call AWS S3 APIs
        return
