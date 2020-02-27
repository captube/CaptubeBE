class Capture:
    def capture(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        captureItems = self._convertToCaptureItems(
            self._executeCaptureScript(url, language, numberToCapture, startTimeStamp, endTimeStamp))
        self._storeImages(captureItems)
        return captureItems

    def _executeCaptureScript(self, url, language, numberToCapture, startTimeStamp, endTimeStamp):
        result = {}
        # TODO Add core logic to capture
        return result

    def _convertToCaptureItems(self, captureItemsByScript):
        convretedItems = {}
        return convretedItems

    def _storeImages(self, captureItems):
        # TODO Call AWS S3 APIs
        return