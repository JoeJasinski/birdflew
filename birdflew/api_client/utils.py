from urllib2 import Request, urlopen, URLError, HTTPError
from lxml import etree

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class ClientParser(object):

    def get_url_as_file(self, url):
        
        neighbor_file = None
    
        req = Request(url)
    
        try:
            response = urlopen(req)
            neighbor_file = StringIO(response.read())
        except HTTPError, e:
            print "HTTP Error:",e.code , url
        except URLError, e:
            print "URL Error:",e.reason , url
            
        return neighbor_file
    
    
    def get_tree_from_file(self, neighbor_file):
        tree = etree.parse(neighbor_file)
        return tree
    
    def get_root_from_tree(self, tree):
        return tree.getroot()

    def get_url_from_root(self, root):
        return root.getchildren()
    
    def get_neighbors_urls(self, url_socket):
        
        url = "%s/lookupurls/" % url_socket 
        neighbor_file = self.get_url_as_file(url)
        tree = self.get_tree_from_file(neighbor_file)
        root = self.get_root_from_tree(tree)
        