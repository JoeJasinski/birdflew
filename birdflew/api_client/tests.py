"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from api_client import utils


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO



class SimpleTest(TestCase):
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ClientTest(TestCase):
    
    def setUp(self):
        self.xml = """<?xml version="1.0" encoding="UTF-8" ?>
            <urls>
              <url>192.168.0.1</url>
              <url>127.0.0.1</url>
            </urls>"""
        

        self.xml_file = StringIO(self.xml)
    
    def test_get_tree_from_file(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        self.assertEqual(1 + 1, 2)
