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
        captureSaver._needSaveVideoMetadata = MagicMock(return_value=True)

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
        captureSaver._needSaveVideoMetadata = MagicMock(return_value=False)

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

    def test__storeImages(self):
        id = "id"
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        fileName1 = "MieyJ34_01.png"
        path1 = f"/home/captube/MieyJ34/imgs/{fileName1}"
        url1 = f"http://captube.net/{fileName1}"
        fileName2 = "MieyJ34_02.png"
        path2 = f"/home/captube/MieyJ34/imgs/{fileName2}"
        url2 = f"http://captube.net/{fileName2}"
        fileName3 = "MieyJ34_03.png"
        path3 = f"/home/captube/MieyJ34/imgs/{fileName3}"
        url3 = f"http://captube.net/{fileName3}"
        fileName4 = "MieyJ34_04.png"
        path4 = f"/home/captube/MieyJ34/imgs/{fileName4}"
        url4 = f"http://captube.net/{fileName4}"
        fileName5 = "MieyJ34_05.png"
        path5 = f"/home/captube/MieyJ34/imgs/{fileName5}"
        url5 = f"http://captube.net/{fileName5}"

        captureItems = [{"id": "id1",
                         "timeStamp": "timeStamp1",
                         "subtitle": "subtitle1",
                         "localFilePath": path1,
                         "saveFileName": fileName1,
                         "url": url1},
                        {"id": "id2",
                         "timeStamp": "timeStamp2",
                         "subtitle": "subtitle2",
                         "localFilePath": path2,
                         "saveFileName": fileName2,
                         "url": url2},
                        {"id": "id3",
                         "timeStamp": "timeStamp3",
                         "subtitle": "subtitle3",
                         "localFilePath": path3,
                         "saveFileName": fileName3,
                         "url": url3},
                        {"id": "id4",
                         "timeStamp": "timeStamp4",
                         "subtitle": "subtitle4",
                         "localFilePath": path4,
                         "saveFileName": fileName4,
                         "url": url4},
                        {"id": "id5",
                         "timeStamp": "timeStamp5",
                         "subtitle": "subtitle5",
                         "localFilePath": path5,
                         "saveFileName": fileName5,
                         "url": url5}]
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
            "url": url2
        }), parse_float=Decimal))

        captureSaver.captionTable.put_item.assert_any_call(Item=json.loads(json.dumps({
            "id": "id3",
            "videoId": "id",
            "timeStamp": "timeStamp3",
            "subtitle": "subtitle3",
            "url": url3
        }), parse_float=Decimal))

        captureSaver.captionTable.put_item.assert_any_call(Item=json.loads(json.dumps({
            "id": "id5",
            "videoId": "id",
            "timeStamp": "timeStamp5",
            "subtitle": "subtitle5",
            "url": url5
        }), parse_float=Decimal))

        captureSaver.s3_client.upload_file.assert_any_call(path2, captureSaver.S3_BUCKET,
                                                           fileName2,
                                                           ExtraArgs={
                                                               'ContentType': 'image/jpeg'
                                                           })
        captureSaver.s3_client.upload_file.assert_any_call(path3, captureSaver.S3_BUCKET,
                                                           fileName3,
                                                           ExtraArgs={
                                                               'ContentType': 'image/jpeg'
                                                           })
        captureSaver.s3_client.upload_file.assert_any_call(path5, captureSaver.S3_BUCKET,
                                                           fileName5,
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
