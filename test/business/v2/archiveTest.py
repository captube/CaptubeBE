import unittest
from unittest.mock import MagicMock

from business.v2.archive import Archive


class archiveTest(unittest.TestCase):
    def test_getArchive(self):
        archive = Archive()
        archiveItem = {
            'id': 'id',
            'title': 'title',
            'thumbnailUrl': 'thumbnailUrl',
            'items': ['caption1', 'caption2', 'caption3']
        }
        captionItem = {
            'id': 'id',
            'url': 'url',
            'timestamp': 'timestamp',
            'subtitle': 'subtitle',
            'videoId': 'videoId'
        }
        archive.editableArchiveTable.get_item = MagicMock(return_value={'Item': archiveItem})
        archive.captionTable.get_item = MagicMock(return_value={'Item': captionItem})

        result = archive.getArchive('arhiveId')

        self.assertEqual({
            'id': 'id',
            'title': 'title',
            'thumbnailUrl': 'thumbnailUrl',
            'items': [captionItem, captionItem, captionItem]
        }, result)

    def test_setArchive(self):
        id = "archiveId"
        title = "title"
        thumbnailUrl = "thumbnailUrl"
        items = []
        archive = Archive()
        archive.editableArchiveTable.put_item = MagicMock()

        archive.setArchive(id, title, thumbnailUrl, items)

        archive.editableArchiveTable.put_item.assert_called_with(Item={
            'id': id,
            'title': title,
            'thumbnailUrl': thumbnailUrl,
            'items': items
        })
