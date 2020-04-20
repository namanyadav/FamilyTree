import unittest

from com.familytree.TreeUtils import get_data_file_path
from com.familytree.stories.UserStoriesDg import UserStoriesDg


class UserStoriesDgTest(unittest.TestCase):
    """ Unittests for userstories 5 and 7 """

    def test_us05(self):
        """ us05 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05(get_data_file_path('us05.ged'))), ['F1', 'F2'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05(get_data_file_path('us05.ged'))), ['US0507F1', 'US0507F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05(get_data_file_path('us05.ged'))), [])

    def test_us07(self):
        """ us07 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07(get_data_file_path('us07.ged'))), ['I1', 'I3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07(get_data_file_path('us07.ged'))), ['US0507I2', 'US0507I3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07(get_data_file_path('us07.ged'))), [])
    
    def test_us12(self):
        """ us12 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us12(get_data_file_path('us12&15.ged'))), ['I20'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us12(get_data_file_path('us12&15.ged'))), ['F1', 'F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us12(get_data_file_path('us12&15.ged'))), [])

    def test_us15(self):
        """ us15 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us15(get_data_file_path('us12&15.ged'))), ['F1'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us15(get_data_file_path('us12&15.ged'))), ['US0507F1', 'US0507F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us15(get_data_file_path('us12&15.ged'))), [])
    
    def test_us23(self):
        """ us23 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us23(get_data_file_path('US23&25.ged'))), ['I3', 'I5', 'I7', 'I9'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us23(get_data_file_path('US23&25.ged'))), ['I3', 'I5'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us23(get_data_file_path('US23&25.ged'))), [])

    def test_us25(self):
        """ us25 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us25(get_data_file_path('US23&25.ged'))), ['F1', 'F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us25(get_data_file_path('US23&25.ged'))), ['F1'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us25(get_data_file_path('US23&25.ged'))), "")

    def test_us33(self):
        """ us33 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us33(get_data_file_path('us33&35.ged'))), ['I5', 'I6'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us33(get_data_file_path('us33&35.ged'))), ['I5'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us33(get_data_file_path('us33&35.ged'))), [])

    def test_us35(self):
        """ us35 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us35(get_data_file_path('us33&35.ged'))), ['I5', 'I6'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us35(get_data_file_path('us33&35.ged'))), ['F1'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us35(get_data_file_path('us33&35.ged'))), "")


if __name__ == "__main__":
    unittest.main()