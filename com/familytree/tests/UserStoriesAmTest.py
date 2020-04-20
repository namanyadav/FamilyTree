import unittest
from com.familytree.stories.UserStoriesAm import UserStoriesAm
from com.familytree.TreeUtils import get_data_file_path

class UserStoriesAmTest(unittest.TestCase):
    """ Unittests for userstories 2 and 6 """

    def test_us02(self):
        """ us02 tests """

        # self.assertEqual(self.get_id_list(UserStoriesAm().us02()), ['US01I5', 'US0206I8', 'US0304I01'])
        self.assertEqual(self.get_id_list(UserStoriesAm().us02()), ['I1', 'I2'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), ['US0910F1', 'US0910F2'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us02()), "")

    def test_us06(self):
        """ us06 tests """

        # self.assertEqual(self.get_id_list(UserStoriesAm().us06()), ['US0206F1','US0206F4'])
        self.assertEqual(self.get_id_list(UserStoriesAm().us06()), ['F2'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us06()), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us06()), "")
    
    def test_us11(self):
        """ us11 tests """

        fp = get_data_file_path('US11and16.ged')
        self.assertEqual(self.get_id_list(UserStoriesAm().us11(fp)), ['I4','I7'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us11(fp)), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us11(fp)), "")

    def test_us16(self):
        """ us16 tests """

        fp = get_data_file_path('US11and16.ged')
        self.assertEqual(self.get_id_list(UserStoriesAm().us16(fp)), ['F1'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us16(fp)), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us16(fp)), "")

    def test_us27(self):
        """ us27 tests """

        fp = get_data_file_path('US27and30.ged')
        self.assertEqual(UserStoriesAm().us27(fp), {'I1': 44, 'I2' : 39,'I3': 19,'I4': 19,'I5': 17,'I6': 16,'I7': 16,'I8': 17})
        self.assertNotEqual(UserStoriesAm().us27(fp), [])
        self.assertNotEqual(UserStoriesAm().us27(fp), "")

    def test_us30(self):
        """ us30 tests """

        fp = get_data_file_path('US27and30.ged')
        self.assertEqual(self.get_id_list(UserStoriesAm().us30(fp)), ['I1','I2','I4','I5','I6','I7'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us30(fp)), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us30(fp)), "")
    
    def test_us34(self):
        """ us34 tests """

        fp = get_data_file_path('US34and36.ged')
        self.assertEqual(self.get_id_list(UserStoriesAm().us34(fp)), ['F1'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us34(fp)), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us34(fp)), "")
    
    def test_us36(self):
        """ us36 tests """

        fp = get_data_file_path('US34and36.ged')
        self.assertEqual(self.get_id_list(UserStoriesAm().us36(fp)), ['I8'])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us36(fp)), [])
        self.assertNotEqual(self.get_id_list(UserStoriesAm().us36(fp)), "")

    
    def get_id_list(self, obj_list):
        """ return the individual or family id's """

        id_list = []
        if obj_list:
            for obj in obj_list:
                id_list.append(obj.id)
        return id_list


if __name__ == "__main__":
    unittest.main()