import unittest

from com.familytree.TreeUtils import get_data_file_path, get_id_list
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK


class UserStoriesMSKTest(unittest.TestCase):
    def setUp(self) -> None:
        """Call before every test case"""
        # print("inside setup")
        self.stories = UserStoriesMSK()

    def tearDown(self) -> None:
        """"Call after every test case"""
        # print("inside teardown")

    def test_us09(self):
        """ US09I1 have failing criteria in us09.ged """
        self.assertEqual(['US09I1'], get_id_list(self.stories.us09(get_data_file_path('us09.ged'))))

    def test_us10(self):
        """ I1, I2, I7 have failing criteria in us10.ged """
        error_list = self.stories.us10(get_data_file_path('us10.ged'))
        self.assertEqual(['F1', 'F2', 'F4'], get_id_list(error_list))

    def test_us17(self):
        """ I3 have failing criteria in us17.ged """
        error_list = self.stories.us17(get_data_file_path('us17.ged'))
        self.assertEqual(['I3'], get_id_list(error_list))

    def test_us18(self):
        """ I1, I2, I6, I8 have failing criteria in us18.ged """
        error_list = self.stories.us18(get_data_file_path('us18.ged'))
        self.assertEqual(['I1', 'I2', 'I6', 'I8'], get_id_list(error_list))

    def test_us20(self):
        """ I10, I4 have failing criteria in US20.ged """
        error_list = self.stories.us20(get_data_file_path('US20.ged'))
        self.assertEqual(['I10', 'I4'], get_id_list(error_list))

    def test_us31(self):
        """ I1, I10, I6 have failing criteria in US31.ged """
        error_list = self.stories.us31(get_data_file_path('US31.ged'))
        self.assertEqual(['I1', 'I10', 'I6'], get_id_list(error_list))

    def test_us38(self):
        """ I1, I3 have failing criteria in US31.ged """
        error_list = self.stories.us38(get_data_file_path('US38.ged'))
        self.assertEqual(['I1', 'I3'], get_id_list(error_list))

    def test_us39(self):
        """ I2, I3, I4 and I5 have failing criteria in US31.ged """
        error_list = self.stories.us39(get_data_file_path('US39.ged'))
        self.assertEqual(['I2', 'I3', 'I4', 'I5'], get_id_list(error_list))


if __name__ == "__main__":
    unittest.main()
