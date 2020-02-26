import unittest
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.TreeLine import TreeLine


class UserStoriesNyTest(unittest.TestCase):
    def setUp(self) -> None:
        """Call before every test case"""
        # print("inside setup")
        self.stories = UserStoriesNy()

    def tearDown(self) -> None:
        """"Call after every test case"""
        # print("inside teardown")

    def test_us01(self):
        """ I1, I5, F1 have failing criteria in us01.ged """
        self.assertEqual(['I1', 'I5', 'F1'], self.get_id_list(self.stories.us01()))
        # self.stories.us01('../data/Family-3-single.ged')

    def test_us08(self):
        """ I6, I7, I8 have failing criteria in us08.ged """
        self.assertEqual(['I5', 'I6', 'I7', 'I8'], self.get_id_list(self.stories.us08()))

    @staticmethod
    def get_id_list(obj_list):
        id_list = []
        for obj in obj_list:
            id_list.append(obj.id)
        return id_list


if __name__ == "__main__":
    unittest.main()
