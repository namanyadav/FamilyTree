<<<<<<< Updated upstream
from com.familytree.stories.UserStoriesNy import UserStoriesNy
from com.familytree.stories.UserStoriesDg import UserStoriesDg
from com.familytree.stories.UserStoriesAm import UserStoriesAm
import os
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
print(sys.executable)
print(os.getcwd())
print(sys.path)
us = UserStoriesNy()
us.us01(os.path.join(os.getcwd(), "com/familytree/data/us01.ged"))
us.us01(os.path.join(os.getcwd(), "com/familytree/data/us08.ged"))
# us.us01(r"C:\Users\divya\OneDrive\Desktop\Stevens\SSW 555\FamilyTree\com\familytree\data\us01.ged")
# us.us08(r"C:\Users\divya\OneDrive\Desktop\Stevens\SSW 555\FamilyTree\com\familytree\data\us08.ged")

us1 = UserStoriesDg()
us1.us05()
us1.us07()

us2 = UserStoriesAm()
us2.us02()
us2.us06()
=======
from com.familytree.stories.UserStoriesMSK import UserStoriesMSK
import os
from os import sys, path

# sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# print(sys.executable)
# print(os.getcwd())
# print(sys.path)
usmsk = UserStoriesMSK()
usmsk.print_list('US 09', usmsk.us09())
# us.us01(r"C:\Users\naman\PycharmProjects\CS-555\com\familytree\data\us01.ged")
# us.us08(r"C:\Users\naman\PycharmProjects\CS-555\com\familytree\data\us08.ged")
#us.log()
>>>>>>> Stashed changes
