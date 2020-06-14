from core.youtube import youtube


class Capture:
    # youtubeObject is need, because we cannot inject core.youtube.youtube.
    # core.youtube.youtube constructor requires url as parameter
    _youtube = None

    def getAvailableLanguage(self, url):
        self._youtube = youtube(url)
        # FIXME: pytube.exceptions.VideoUnavailable: fTTGALaRZoc is unavailable
        caption = self._youtube.get_captions()
        return {
            "languages": self._youtube.get_available_langs(caption)
        }
