import unittest
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
        self.assertEqual(['US09I1'], self.get_id_list(self.stories.us09('../data/us09.ged')))
        # self.stories.us01('../data/Family-3-single.ged')

    def test_us10(self):
        """ I1, I2, I7 have failing criteria in us10.ged """
        error_list = self.stories.us10('../data/us10.ged')
        self.assertEqual(['F1', 'F2', 'F4'], self.get_id_list(error_list))

    @staticmethod
    def get_id_list(obj_list):
        id_list = []
        for obj in obj_list:
            print(obj.id)
            id_list.append(obj.id)
        return id_list


if __name__ == "__main__":
    unittest.main()
