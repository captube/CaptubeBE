import json
import unittest
from decimal import Decimal
from unittest.mock import MagicMock

from business.common.CaptureSaver import CaptureSaver


class CaptureSaverTest(unittest.TestCase):
    def test_save(self):
        captureInformation = []
        captureSaver = CaptureSaver()
        captureSaver._storeImages = MagicMock(return_value=captureInformation)
        captureSaver._storeVideoMetadata = MagicMock(return_value={})

        captureSaver.save(captureInformation)

        captureSaver._storeVideoMetadata.assert_called_with(captureInformation)
        captureSaver._storeImages.assert_called_with(captureInformation)

    def test__storeVideoMetadata(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"}]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver.videoTable = MagicMock()
        captureSaver.videoTable.put_item = MagicMock(return_value={})
        captureSaver.captionTable = MagicMock()
        captureSaver.captionTable.put_item = MagicMock(return_value={})
        captureSaver._needSaveMetadata = MagicMock(return_value=True)

        captureSaver._storeVideoMetadata(captureInformation)

        captureSaver.videoTable.put_item.assert_called_with(Item={
            'id': captureInformation['id'],
            'title': captureInformation['title'],
            'thumbnailUrl': captureInformation['thumbnailUrl']
        })

    def test__storeVideoMetadata_when_dont_need(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"}]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver.videoTable = MagicMock()
        captureSaver.videoTable.put_item = MagicMock(return_value={})
        captureSaver.captionTable = MagicMock()
        captureSaver.captionTable.put_item = MagicMock(return_value={})
        captureSaver._needSaveMetadata = MagicMock(return_value=False)

        captureSaver._storeVideoMetadata(captureInformation)

        captureSaver.videoTable.put_item.assert_not_called()

    def test__needSaveVideoMetadata(self):
        captureSaver = CaptureSaver()
        captureSaver._getVideo = MagicMock(return_value=None)

        result = captureSaver._needSaveVideoMetadata("id")

        self.assertTrue(result)

    def test__needSaveVideoMetadata_not(self):
        captureSaver = CaptureSaver()
        captureSaver._getVideo = MagicMock(return_value={})

        result = captureSaver._needSaveVideoMetadata("id")

        self.assertFalse(result)

    def test__convertAsS3Url(self):
        fileName = "MieyJ34_01.png"
        captureSaver = CaptureSaver()

        convertedPath = captureSaver._convertAsS3Url(fileName)

        self.assertEqual(f'{captureSaver.S3_PREFIX}{fileName}', convertedPath)

    def test__storeImages(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        fileName1 = "MieyJ34_01.png"
        path1 = f"/home/captube/MieyJ34/imgs/{fileName1}"
        fileName2 = "MieyJ34_02.png"
        path2 = f"/home/captube/MieyJ34/imgs/{fileName2}"
        fileName3 = "MieyJ34_03.png"
        path3 = f"/home/captube/MieyJ34/imgs/{fileName3}"
        fileName4 = "MieyJ34_04.png"
        path4 = f"/home/captube/MieyJ34/imgs/{fileName4}"
        fileName5 = "MieyJ34_05.png"
        path5 = f"/home/captube/MieyJ34/imgs/{fileName5}"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "path": path1},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "path": path2},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "path": path3},
                        {"id": "id4",
                         "timeStamp": "timeStamp4",
                         "subtitle": "subtitle4",
                         "path": path4},
                        {"id": "id5",
                         "timeStamp": "timeStamp5",
                         "subtitle": "subtitle5",
                         "path": path5}]
        storedCaptureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver._getToSaveCaptures = MagicMock(return_value=[captureItems[1], captureItems[2], captureItems[4]])
        captureSaver.s3_client = MagicMock()
        captureSaver.s3_client.upload_file = MagicMock()
        captureSaver.captionTable.put_item = MagicMock(return_value={})

        captureSaver._storeImages(storedCaptureInformation)

        captureSaver.captionTable.put_item.assert_any_call(Item=json.loads(json.dumps({
            "id": "id2",
            "videoId": "id",
            "timeStamp": "timeStamp2",
            "subtitle": "subtitle2",
            "url": captureSaver._convertAsS3Url(f'id_{fileName2}')
        }), parse_float=Decimal))

        captureSaver.captionTable.put_item.assert_any_call(Item=json.loads(json.dumps({
            "id": "id3",
            "videoId": "id",
            "timeStamp": "timeStamp3",
            "subtitle": "subtitle3",
            "url": captureSaver._convertAsS3Url(f'id_{fileName3}')
        }), parse_float=Decimal))

        captureSaver.captionTable.put_item.assert_any_call(Item=json.loads(json.dumps({
            "id": "id5",
            "videoId": "id",
            "timeStamp": "timeStamp5",
            "subtitle": "subtitle5",
            "url": captureSaver._convertAsS3Url(f'id_{fileName5}')
        }), parse_float=Decimal))

        captureSaver.s3_client.upload_file.assert_any_call(path2, captureSaver.S3_BUCKET,
                                                           f'{storedCaptureInformation["id"]}_{fileName2}',
                                                           ExtraArgs={
                                                               'ContentType': 'image/jpeg'
                                                           })
        captureSaver.s3_client.upload_file.assert_any_call(path3, captureSaver.S3_BUCKET,
                                                           f'{storedCaptureInformation["id"]}_{fileName3}',
                                                           ExtraArgs={
                                                               'ContentType': 'image/jpeg'
                                                           })
        captureSaver.s3_client.upload_file.assert_any_call(path5, captureSaver.S3_BUCKET,
                                                           f'{storedCaptureInformation["id"]}_{fileName5}',
                                                           ExtraArgs={
                                                               'ContentType': 'image/jpeg'
                                                           })

    def test__getToSaveCaptions(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "url": "url3"}
                        ]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver._getCaptions = MagicMock(return_value=[{'id': 'id1'}])

        result = captureSaver._getToSaveCaptures(captureInformation)
        captureSaver._getCaptions.asset_called_with("id", "timpeStamp1", "timpeStamp3")

        self.assertEqual("id2", result[0]["id"])
        self.assertEqual("id3", result[1]["id"])

    def test__getToSaveCaptions_2(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "url": "url3"}
                        ]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver._getCaptions = MagicMock(return_value=[{'id': 'id2'}])

        result = captureSaver._getToSaveCaptures(captureInformation)
        captureSaver._getCaptions.asset_called_with("id", "timpeStamp1", "timpeStamp3")

        self.assertEqual("id1", result[0]["id"])
        self.assertEqual("id3", result[1]["id"])

    def test__getToSaveCaptions_3(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "url": "url3"}
                        ]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver._getCaptions = MagicMock(return_value=[])

        result = captureSaver._getToSaveCaptures(captureInformation)
        captureSaver._getCaptions.asset_called_with("id", "timpeStamp1", "timpeStamp3")

        self.assertEqual("id1", result[0]["id"])
        self.assertEqual("id2", result[1]["id"])
        self.assertEqual("id3", result[2]["id"])

    def test__getToSaveCaptions_4(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "url": "url1"},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "url": "url2"},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "url": "url3"}
                        ]
        captureInformation = {
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'captureItems': captureItems
        }
        captureSaver = CaptureSaver()
        captureSaver._getCaptions = MagicMock(return_value=[ \
            {"id": "id1"}, {"id": "id2"}, {"id": "id3"}])

        result = captureSaver._getToSaveCaptures(captureInformation)
        captureSaver._getCaptions.asset_called_with("id", "timpeStamp1", "timpeStamp3")

        self.assertEqual(0, len(result))
