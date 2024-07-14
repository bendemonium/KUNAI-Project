import sys
import os
from unittest import TestCase

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

# Define a base test case class with common setup
class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # This method is called once before any tests in the class are run
        # You can set up any shared resources here
        pass

    @classmethod
    def tearDownClass(cls):
        # This method is called once after all tests in the class have been run
        # You can clean up any shared resources here
        pass

    def setUp(self):
        # This method is called before each test method
        # You can set up any per-test resources here
        pass

    def tearDown(self):
        # This method is called after each test method
        # You can clean up any per-test resources here
        pass

# You can add any other common test utilities or configurations here