from core import capture
from core import run


class CaptureRunner:
    RESULT_DIR = "results"

    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp, workingPath):
        print(f'capture, {url}, {language}, {numberToCapture}, {startTimeStamp}, {endTimeStamp}')

        videoInformation = self._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp,
                                                      workingPath)

        return videoInformation

    def _executeCaptureScript(self, url, language, numberToCapture, startTimeStamp, endTimeStamp, name):
        print(f'execute capture script, {url}, {language}, {numberToCapture}, {startTimeStamp}, {endTimeStamp}, {name}')
        videoInformation = run.make_youtube_info(url, name, language)
        videoInformation.save_json()
        capture.capture_by_subs(videoInformation)
        print(f'video_info : {videoInformation}')
        return videoInformation
