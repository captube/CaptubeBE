import unittest

from business.common.YoutubeIdParser import YoutubeIdParser


class YoutubeIdParserTest(unittest.TestCase):
    def test(self):
        youtubeIdParser = YoutubeIdParser()

        id = youtubeIdParser.parse("https://youtu.be/PLZV9Aj0e1Q")
        self.assertEqual("PLZV9Aj0e1Q", id)

        id = youtubeIdParser.parse("https://youtu.be/EpcaAM1Lf94?list=RDMMCYm6U1L9068")
        self.assertEqual("EpcaAM1Lf94", id)

        id = youtubeIdParser.parse("https://youtu.be/LSuTlGfl1y8?list=RDMMCYm6U1L9068")
        self.assertEqual("LSuTlGfl1y8", id)

        id = youtubeIdParser.parse("https://youtu.be/PLZV9Aj0e1Q")
        self.assertEqual("PLZV9Aj0e1Q", id)
