import unittest
from com.familytree.stories.UserStoriesDg import UserStoriesDg


class UserStoriesDgTest(unittest.TestCase):
    """ Unittests for userstories 5 and 7 """

    def test_us05(self):
        """ us05 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), ['F1', 'F2'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), ['US0507F1', 'US0507F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), [])

    def test_us07(self):
        """ us07 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), ['I1', 'I3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), ['US0507I2', 'US0507I3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), [])


if __name__ == "__main__":
    unittest.main()