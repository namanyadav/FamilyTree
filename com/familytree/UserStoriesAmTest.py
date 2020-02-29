import unittest
from UserStoriesAm import UserStoriesAm

class UserStoriesAmTest(unittest.TestCase):
    """ Unittests for userstories 2 and 6 """

    def test_us02(self):
        """ us02 tests """

        self.assertEqual(self.get_id_list(UserStoriesAm().us02()), ['I8'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), ['F1', 'F2'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), "")

    def test_us06(self):
        """ us06 tests """

        self.assertEqual(self.get_id_list(UserStoriesAm().us06()), ['F1','F4'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us06()), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us06()), "")
    
    def get_id_list(self, obj_list):
        """ return the individual or family id's """

        id_list = []
        if obj_list:
            for obj in obj_list:
                id_list.append(obj.id)
        return id_list

if __name__ == "__main__":
    unittest.main()