import unittest
from com.familytree.stories.UserStoriesAm import UserStoriesAm

class UserStoriesAmTest(unittest.TestCase):
    """ Unittests for userstories 2 and 6 """

    def test_us02(self):
        """ us02 tests """

        self.assertEqual(self.get_id_list(UserStoriesAm().us02()), ['US01I5', 'US0206I8', 'US0910I11'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), ['US0910F1', 'US0910F2'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), "")

    def test_us06(self):
        """ us06 tests """

        self.assertEqual(self.get_id_list(UserStoriesAm().us06()), ['US0206F1','US0206F4'])
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