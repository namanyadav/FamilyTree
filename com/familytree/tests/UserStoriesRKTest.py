import unittest
from com.familytree.stories.UserStoriesRK import UserStoriesRK

class UserStoriesRKTest(unittest.TestCase):
    """ Unit Testing for US 03 & US 04"""
    def test_us03(self):
        """ testing us03"""
        self.assertEqual(UserStoriesRK().get_id_list(UserStoriesRK().us03()), ['I01'])
        self.assertNotEqual(UserStoriesRK().get_id_list(UserStoriesRK().us03()), ['I01', 'I03'])

    def test_us04(self):
        """testing us04"""
        self.assertEqual(UserStoriesRK().get_id_list(UserStoriesRK().us04()), ['F04'])
        self.assertNotEqual(UserStoriesRK().get_id_list(UserStoriesRK().us04()), ['F04', 'F01'])

if __name__ == '__main__':
    unittest.main()

