import unittest
from unittest.mock import MagicMock

from boto3.dynamodb.conditions import Attr

from business.v1.archive import Archive
from business.v1.archive import archiveTable
from business.v1.archive import captureItemTable


class TestArchive(unittest.TestCase):

    def test_getPagedArchive(self):
        archive = Archive()
        archives = []
        lastEvaluatedKey = {}
        pageSize = 10
        archivesFromAWS = {'Items': archives, 'LastEvaluatedKey': lastEvaluatedKey}
        archiveTable.scan = MagicMock(return_value=archivesFromAWS)

        response = archive.getPagedArchive(None, None)

        archiveTable.scan.assert_called_with(Limit=archive._DEFAULT_PAGE_SIZE)
        self.assertEqual({'archives': archivesFromAWS['Items'], 'nextPageKey': archivesFromAWS['LastEvaluatedKey']},
                         response)

        response = archive.getPagedArchive(lastEvaluatedKey, None)

        archiveTable.scan.assert_called_with(Limit=archive._DEFAULT_PAGE_SIZE, ExclusiveStartKey=lastEvaluatedKey)
        self.assertEqual({'archives': archivesFromAWS['Items'], 'nextPageKey': archivesFromAWS['LastEvaluatedKey']},
                         response)

        response = archive.getPagedArchive(None, pageSize)

        archiveTable.scan.assert_called_with(Limit=pageSize)
        self.assertEqual({'archives': archivesFromAWS['Items'], 'nextPageKey': archivesFromAWS['LastEvaluatedKey']},
                         response)

        response = archive.getPagedArchive(lastEvaluatedKey, pageSize)

        archiveTable.scan.assert_called_with(Limit=pageSize, ExclusiveStartKey=lastEvaluatedKey)
        self.assertEqual({'archives': archivesFromAWS['Items'], 'nextPageKey': archivesFromAWS['LastEvaluatedKey']},
                         response)

    def test_getPagedArchive_to_end(self):
        archive = Archive()
        archives = []
        lastEvaluatedKey = "LastEvaluatedKey"
        pageSize = 10
        archivesFromAWS = {'Items': archives}
        archiveTable.scan = MagicMock(return_value=archivesFromAWS)

        response = archive.getPagedArchive(None, None)

        archiveTable.scan.assert_called_with(Limit=archive._DEFAULT_PAGE_SIZE)
        self.assertEqual({'archives': archivesFromAWS['Items']}, response)

        response = archive.getPagedArchive(lastEvaluatedKey, None)

        archiveTable.scan.assert_called_with(Limit=archive._DEFAULT_PAGE_SIZE, ExclusiveStartKey=lastEvaluatedKey)
        self.assertEqual({'archives': archivesFromAWS['Items']}, response)

        response = archive.getPagedArchive(None, pageSize)

        archiveTable.scan.assert_called_with(Limit=pageSize)
        self.assertEqual({'archives': archivesFromAWS['Items']}, response)

        response = archive.getPagedArchive(lastEvaluatedKey, pageSize)

        archiveTable.scan.assert_called_with(Limit=pageSize, ExclusiveStartKey=lastEvaluatedKey)
        self.assertEqual({'archives': archivesFromAWS['Items']}, response)

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
