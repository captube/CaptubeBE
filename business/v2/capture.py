import os
import shutil
import uuid

from business import session
from business.common.CaptureRunner import CaptureRunner
from business.common.CaptureSaver import CaptureSaver
from business.common.YoutubeIdParser import YoutubeIdParser
from core.youtube import youtube


class Capture:
    RESULT_DIR = "results"
    S3_BUCKET = "captube.captures"
    S3_PREFIX = "https://s3.ap-northeast-2.amazonaws.com/captube.captures/"
    dynamodb = session.resource('dynamodb', region_name='ap-northeast-2')
    # TODO : Need DI
    youtubeIdParser = YoutubeIdParser()
    captureRunner = CaptureRunner()
    captureSaver = CaptureSaver()

    s3_client = session.client('s3')

    # youtubeObject is need, because we cannot inject core.youtube.youtube.
    # core.youtube.youtube constructor requires url as parameter
    _youtube = None

    def getAvailableLanguage(self, url):
        try:
            self._youtube = youtube(url)
            # FIXME: pytube.exceptions.VideoUnavailable: fTTGALaRZoc is unavailable
            caption = self._youtube.get_captions()
        except Exception as e:
            print(f'Exception occurred during get languages {e}')
            raise e

        return {
            "languages": self._youtube.get_available_langs(caption)
        }

    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        print(f'capture, {url}, {language}, {numberToCapture}, {startTimeStamp}, {endTimeStamp}')
        id = str(f'{self.youtubeIdParser.parse(url)}_{language}')
        workingPath = str(uuid.uuid4())

        try:
            videoInformation = self.captureRunner.capture(url, language, numberToCapture, startTimeStamp, endTimeStamp,
                                                          workingPath)
            captureInformation = self._asCaptureInformation(videoInformation, id)
            self.captureSaver.save(captureInformation)
        except Exception as e:
            print(f'Exception occurred during capture {e}')
            raise e
        finally:
            self._clearLocalTemporary(workingPath)

        return captureInformation

    def _asCaptureInformation(self, captureResultByScript, id):
        result = {
            "title": captureResultByScript["title"],
            "thumbnailUrl": captureResultByScript["thumbnail"],
            "id": id,
            "captureItems": []
        }

        frame_infos = captureResultByScript["frame_infos"]

        for frame_info in frame_infos:
            id = f'{result["id"]}_{frame_info["frame_num"]}'
            frameNumber = frame_info["frame_num"]
            path = frame_info["img_path"]
            noSubtitlePath = self._getNoSubtitleImagePath(frame_info["img_path"])
            fileName = f'{result["id"]}_{os.path.basename(path)}'
            noSubtitleFileName = f'noSub_{result["id"]}_{os.path.basename(noSubtitlePath)}'
            url = self._convertAsS3Url(fileName)
            noSubtitleUrl = self._convertAsS3Url(noSubtitleFileName)

            result["captureItems"].append({
                "id": id,
                "frameNumber": frameNumber,
                "url": url,
                "noSubtitleUrl": noSubtitleUrl,
                "localFilePath": path,
                "localNoSubtitleFilePath": noSubtitlePath,
                "saveFileName": fileName,
                "noSubtitleSaveFileName": noSubtitleFileName,
                # TODO : video information should provide time stamp
                # "timeStamp": frame_info["time_info"],
                "timeStamp": 0,
                "subtitle": frame_info["script"]
            })

        return result

    def _convertAsS3Url(self, fileName):
        return f'{self.S3_PREFIX}{fileName}'

    def _getNoSubtitleImagePath(self, imagePath):
        return f'{os.path.dirname(imagePath)}/nosub/{os.path.basename(imagePath)}'

    def _clearLocalTemporary(self, id):
        shutil.rmtree(f'{self.RESULT_DIR}/{id}')
        return
