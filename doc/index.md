# Birdflew Peer-to-Peer Social Bookmark Project
## SE560

### Report Draft

#### Summary 

The hostname for this node currently resides at http://ec2-50-19-183-238.compute-1.amazonaws.com.  Time permitting, I intend to give it a shorter domain.  

Currently, the node is being hosted off of an amazon ec2 instance.  The application is built using the Python-based web framework Django.  It uses the Nginx webserver for static content hosting, fastcgi/flup for dynamic content, PostgreSQL for the persistence layer, lxml for xml parsing/rendering, and redis for caching.  

Currently, the main user that I have on the site by default is joe@joe.com.  This user can be accessed by querying the following url:

http://ec2-50-19-183-238.compute-1.amazonaws.com/v2/users/joe@joe.com

The current API methods are functioning according to the specification.  They probably need a bit more debugging but are working as far as I am aware.  Most of the v2 GET urls support a .xml extension to display the data in xml format.  By default, urls are stored in 

#### Features
1. Support for xhtml microformat output
2. Admin Interface for browsing persisted data (at /admin/). 
3. Status page at site root (/) displaying neighbor node status
4. XML RelaxNG validation of POSTed data
5. Programmatically created XML
6. XML to XHTML conversion using XSLT

#### URL Methods

-   /v1/whoami     GET 
--   Input: none
--   Output: plain text email of node owner

-   /v1/lookupUrls  GET 
--  Input: none
--  Output:  List of node urls
    <urls>
        <url>http://50.17.226.103:80</url>
        <url>http://afternoon-snow-4694.herokuapp.com:80</url>
        ....
    </urls>

-   /v1/registerUrls  POST

-   /v2/users  GET
-- Input: none
-- Output: List of users 

-   /v2/users  POST
--  Input: 
    <user>
        <email>bob@whitequail.org</email>
        <node>http://bobs-whizbang.elasticbeanstalk.com</node>
    </user>
-- Output: 
    <?xml version="1.0" encoding="utf-8"?>
        <message><success>User Added</success>
    </message>

-   /v2/users/{username}  GET
-- Input: none
-- Output: user detail for a specific user

-   /v2/users/{username}/urls  GET
-- Input: none
-- Output: list all users urls

-   /v2/users/{username}/urls  POST
-- Input: a required uri, an optional list of categories, and an optional list of comments
    <url>
        <uri>http://somewhere.com</uri>
        <categories>
           <category>News</category>
           <category>Sports</category>
        </categories>
        <comments>
           <comment>This is comment 1</comment>
           <comment>This is comment 2</comment>
        </comments>
    </url>
-- Output: 
    <?xml version="1.0" encoding="utf-8"?><message><success>Bookmark Added</success></message>

-   /v2/users/{username}/urls/{url_id}  GET
-- Input: none
-- Output: a specific url for a given user

-   /v2/categories  GET
-- Input: none
-- Output: a list of available categories 

-   /v2/categories/{category}  GET
-- Input: none
-- Output: details about a category

-   /v2/users/{username}/subscribe  POST
-- input: 
    <subscribe>
        <callback-url>http://examplenode.org/v2/users/alice@springs.com/notify</callback-url>
    </subscribe>
-- Output:
    <?xml version="1.0" encoding="utf-8"?><message><success>Subscription added</success></message>


#### TODO

1. Basic support for the callback notifications exist, but need more debugging.
2. Need to implement GET /v2/users/{user}/notifications
3. More testing needed
