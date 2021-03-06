import unittest

from openprocurement_client.tests import (
    tests_resources,
    tests_sync,
    test_registry_client,
    tests_dasu,
    tests_utils
)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(tests_sync.suite())
    suite.addTest(test_registry_client.suite())
    suite.addTest(tests_resources.suite())
    suite.addTest(tests_dasu.suite())
    suite.addTest(tests_utils.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
