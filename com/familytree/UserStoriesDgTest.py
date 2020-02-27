import unittest
from UserStoriesDg import UserStoriesDg

class UserStoriesDgTest(unittest.TestCase):
    """ Unittests for userstories 5 and 7 """

    def test_us05(self):
        """ us05 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), ['F2', 'F3', 'F4'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), ['F1', 'F3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us05()), [])

    def test_us07(self):
        """ us07 tests """

        self.assertEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), ['I1'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), ['I2', 'I3'])
        self.assertNotEqual(UserStoriesDg().get_id_list(UserStoriesDg().us07()), [])

if __name__ == "__main__":
    unittest.main()