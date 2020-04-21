import unittest
from com.familytree.TreeUtils import get_id_list, get_data_file_path
from com.familytree.stories.UserStoriesRK import UserStoriesRK


class UserStoriesRKTest(unittest.TestCase):
    """ Unit Testing for US 03 & US 04"""
    def test_us03(self):
        """ testing us03"""
        self.assertEqual(UserStoriesRK().get_id_list(UserStoriesRK().us03()), ['I01'])
        self.assertNotEqual(UserStoriesRK().get_id_list(UserStoriesRK().us03()), ['I01', 'I03'])

    def test_us04(self):
        """testing us04"""
        self.assertEqual(get_id_list(UserStoriesRK().us04()), ['F04'])
        self.assertNotEqual(get_id_list(UserStoriesRK().us04()), ['F04', 'F01'])

    def test_us14(self):
        """ testing us14"""
        fp = get_data_file_path('US14.ged')
        self.assertEqual(UserStoriesRK().get_id_list(UserStoriesRK().us14(fp)), ['F1'])
        self.assertNotEqual(UserStoriesRK().get_id_list(UserStoriesRK().us14(fp)), ['I01', 'I03'])

    def test_us21(self):
        """testing us21"""
        fp = get_data_file_path('US14.ged')
        self.assertEqual(get_id_list(UserStoriesRK().us21(fp)), ['F1'])
        self.assertNotEqual(get_id_list(UserStoriesRK().us21(fp)), ['F04', 'F01'])

    def test_us28(self):
        """ testing us28"""
        fp = get_data_file_path('us28.ged')
        self.assertEqual(UserStoriesRK().us28(fp), [['I7', 'I8', 'I9'], ['I3', 'I4', 'I5']])
        self.assertNotEqual(UserStoriesRK().us28(fp), ['I01', 'I03'])

    def test_us29(self):
        """testing us29"""
        fp = get_data_file_path('us03&04.ged')
        self.assertEqual(get_id_list(UserStoriesRK().us29(fp)), ['I01', 'I08'])
        self.assertNotEqual(get_id_list(UserStoriesRK().us29(fp)), ['I01', 'F01'])

    def test_us24(self):
        """ testing us24"""
        fp = get_data_file_path('us24.ged')
        self.assertEqual(get_id_list(UserStoriesRK().us24(fp)), ['F2'])
        self.assertNotEqual(get_id_list(UserStoriesRK().us24(fp)), ['F1'])

    def test_us32(self):
        """testing us32"""
        fp = get_data_file_path('US14.ged')
        self.assertEqual(get_id_list(UserStoriesRK().us32(fp)), ['F1'])
        self.assertNotEqual(get_id_list(UserStoriesRK().us32(fp)), ['I01', 'F01'])



if __name__ == '__main__':
    unittest.main()

