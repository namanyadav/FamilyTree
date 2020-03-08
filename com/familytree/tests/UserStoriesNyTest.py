import unittest
from com.familytree.TreeUtils import get_data_file_path, get_id_list
from com.familytree.stories.UserStoriesNy import UserStoriesNy


class UserStoriesNyTest(unittest.TestCase):
    def setUp(self) -> None:
        """ Call before every test case """
        # print("inside setup")
        self.stories = UserStoriesNy()

    def tearDown(self) -> None:
        """" Call after every test case """
        # print("inside teardown")

    def test_us01(self):
        """ I1, I5, F1 have failing criteria in us01.ged """
        self.assertEqual(['I1', 'I5', 'F1'], get_id_list(self.stories.us01(get_data_file_path('us01.ged'))))

    def test_us08(self):
        """ I5, I6, I7, I8 have failing criteria in us08.ged """
        self.assertEqual(['I5', 'I6', 'I7', 'I8'], get_id_list(self.stories.us08(get_data_file_path('us08.ged'))))

    def test_us13(self):
        self.assertEqual(['I1', 'I10', 'I5', 'I7'], get_id_list(self.stories.us13(get_data_file_path('us13.ged'))))

    def test_us19(self):
        self.assertEqual(['I12', 'I8'], get_id_list(self.stories.us19(get_data_file_path('us19.ged'))))


if __name__ == "__main__":
    unittest.main()
