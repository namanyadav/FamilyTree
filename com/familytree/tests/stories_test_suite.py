import unittest

from com.familytree.tests.UserStoriesAmTest import UserStoriesAmTest
from com.familytree.tests.UserStoriesDgTest import UserStoriesDgTest
from com.familytree.tests.UserStoriesMSKTest import UserStoriesMSKTest
from com.familytree.tests.UserStoriesNyTest import UserStoriesNyTest
from com.familytree.tests.UserStoriesRKTest import UserStoriesRKTest


def suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(UserStoriesNyTest('test_us01'))
    test_suite.addTest(UserStoriesNyTest('test_us08'))
    test_suite.addTest(UserStoriesNyTest('test_us13'))
    test_suite.addTest(UserStoriesNyTest('test_us19'))
    test_suite.addTest(UserStoriesNyTest('test_us22'))
    test_suite.addTest(UserStoriesNyTest('test_us26'))
    test_suite.addTest(UserStoriesNyTest('test_us37'))
    test_suite.addTest(UserStoriesNyTest('test_us40'))

    test_suite.addTest(UserStoriesRKTest('test_us03'))
    test_suite.addTest(UserStoriesRKTest('test_us04'))
    test_suite.addTest(UserStoriesRKTest('test_us14'))
    test_suite.addTest(UserStoriesRKTest('test_us21'))
    test_suite.addTest(UserStoriesRKTest('test_us28'))
    test_suite.addTest(UserStoriesRKTest('test_us29'))

    test_suite.addTest(UserStoriesDgTest('test_us05'))
    test_suite.addTest(UserStoriesDgTest('test_us07'))
    test_suite.addTest(UserStoriesDgTest('test_us12'))
    test_suite.addTest(UserStoriesDgTest('test_us15'))
    test_suite.addTest(UserStoriesDgTest('test_us23'))
    test_suite.addTest(UserStoriesDgTest('test_us25'))
    test_suite.addTest(UserStoriesDgTest('test_us33'))
    test_suite.addTest(UserStoriesDgTest('test_us35'))

    test_suite.addTest(UserStoriesMSKTest('test_us09'))
    test_suite.addTest(UserStoriesMSKTest('test_us10'))
    test_suite.addTest(UserStoriesMSKTest('test_us17'))
    test_suite.addTest(UserStoriesMSKTest('test_us18'))
    test_suite.addTest(UserStoriesMSKTest('test_us20'))
    test_suite.addTest(UserStoriesMSKTest('test_us31'))

    test_suite.addTest(UserStoriesAmTest('test_us02'))
    test_suite.addTest(UserStoriesAmTest('test_us06'))
    test_suite.addTest(UserStoriesAmTest('test_us11'))
    test_suite.addTest(UserStoriesAmTest('test_us16'))
    test_suite.addTest(UserStoriesAmTest('test_us27'))
    test_suite.addTest(UserStoriesAmTest('test_us30'))
    test_suite.addTest(UserStoriesAmTest('test_us34'))
    test_suite.addTest(UserStoriesAmTest('test_us36'))

    return test_suite


def suite_loader():
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)
    all_test_suite_disvoery = unittest.defaultTestLoader.discover('.', pattern='*Test.py')
    for all_test_suite in all_test_suite_disvoery:
        for test_suite in all_test_suite:
            suite.addTests(test_suite)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

# python -m com.familytree.tests.UserStoriesNyTest
# python -m com.familytree.tests.stories_test_suite
