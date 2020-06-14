import unittest


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
