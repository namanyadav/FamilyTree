import unittest
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.TreeLine import TreeLine


class UserStoriesNyTest(unittest.TestCase):
    def setUp(self) -> None:
        """Call before every test case"""
        print("inside setup")
        fam_heading_list = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                            "Children", "Warning"]
        indi_heading_list = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse", "Warning"]
        self.story = UserStoriesNy()
        self.fam_table_printer = TreeLine().get_table_printer('FAM', fam_heading_list)
        self.indi_table_printer = TreeLine().get_table_printer('INDI', indi_heading_list)

    def tearDown(self) -> None:
        """"Call after every test case"""
        print("inside teardown")


    def test_us01(self):
        """ method to test US01 """
        file_path = self.story.get_file_path('us01')
        processed_tree = TreeLine().process_data(file_path)
        indi_i1 = processed_tree.get('I1')
        indi_i5 = processed_tree.get('I5')
        self.assertEqual([indi_i1.id, indi_i5.id], self.get_id_list(self.story.us01()))

    def test_us08(self):
        """ method to test US08 """
        file_path = self.story.get_file_path('us08')
        family_tree = TreeLine().process_data(file_path)
        i1 = family_tree.get('i1')
        i10 = family_tree.get('i10')
        i4 = family_tree.get('i4')
        self.assertEqual([i1.id, i10.id, i4.id], self.get_id_list(self.story.us08()))

    @staticmethod
    def get_id_list(obj_list):
        id_list = []
        for obj in obj_list:
            id_list.append(obj.id)
        return id_list


if __name__ == "__main__":
    unittest.main()