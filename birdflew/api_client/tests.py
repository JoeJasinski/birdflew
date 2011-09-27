"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.test import TestCase, Client
from api_client import utils
from lxml import etree

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
        self.assertTrue(tree, etree._Element)
 

    def test_get_root_from_tree(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        root = c.get_root_from_tree(tree)
        self.assertEqual(root.tag, 'urls')
        self.assertTrue(root, etree._Element)


    def test_get_url_from_root(self):
        c = utils.ClientParser()
        tree = c.get_tree_from_file(self.xml_file)
        root = c.get_root_from_tree(tree)
        children = c.get_url_from_root(root)
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].tag == 'url')
        self.assertTrue(children[1].tag == 'url')
        self.assertTrue(isinstance(children[0], etree._Element))
        
        
    def test_get_url(self):
        test_client = Client()
        request = test_client.get(reverse('api_lookupurls'))
        c = utils.ClientParser()
        tree = c.get_tree_from_file(StringIO(request.content))
        root = c.get_root_from_tree(tree)
        children = c.get_url_from_root(root)
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].tag == 'url')
        self.assertTrue(children[1].tag == 'url')
        self.assertTrue(isinstance(children[0], etree._Element))
                
    def test_get_url_2(self):
        c = utils.ClientParser()
        file = c.get_url_as_file("http://%s/%s" % (Site.objects.get_current(), reverse('api_lookupurls')))
        tree = c.get_tree_from_file(file)
        root = c.get_root_from_tree(tree)
        children = c.get_url_from_root(root)
        self.assertTrue(len(children) == 2)
        self.assertTrue(children[0].tag == 'url')
        self.assertTrue(children[1].tag == 'url')
        self.assertTrue(isinstance(children[0], etree._Element))        
        