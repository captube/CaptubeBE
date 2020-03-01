import unittest
from unittest.mock import MagicMock

from boto3.dynamodb.conditions import Attr

from business.v1.archive import Archive
from business.v1.archive import archiveTable
from business.v1.archive import captureItemTable


class TestArchive(unittest.TestCase):

    def test_archiveid(self):
        archive = Archive()
        id = 'id'
        archiveTitle = 'archiveTitle'
        archiveId = 'archiveId'
        archiveFromAWS = {'Item': {'id': archiveId, 'title': archiveTitle}}
        captureItemsFromAWS = {'Items': []}
        archiveTable.get_item = MagicMock(return_value=archiveFromAWS)
        captureItemTable.scan = MagicMock(return_value=captureItemsFromAWS)

        response = archive.getArchive(id)

        archiveTable.get_item.assert_called_with(Key={'id': id})
        captureItemTable.scan.assert_called_with(FilterExpression=Attr('archiveId').eq(archiveId))
        self.assertEqual({'title': archiveTitle, 'items': captureItemsFromAWS['Items']}, response)