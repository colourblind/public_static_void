import xml.etree.ElementTree as et
from datetime import datetime
from sqlalchemy import *

class Post:
    def __init__(self):
        self.title = ''
        self.body = ''
        self.created_date = None
        
    def __repr__(self):
        return '{0} - {1}'.format(self.title, self.created_date)
        
    @staticmethod
    def from_rss(node):
        post = Post()
        post.title = node.findtext('title')
        post.body = node.findtext('description')
        post.created_date = datetime.strptime(node.findtext('pubDate'), '%a, %d %b %Y %H:%M:%S %Z')
        return post
        
    @staticmethod
    def from_blogml(node):
        post = Post()
        post.title = node.findtext('{http://www.blogml.com/2006/09/BlogML}title')
        post.body = node.findtext('{http://www.blogml.com/2006/09/BlogML}content')
        post.created_date = datetime.strptime(node.attrib['date-created'], '%Y-%m-%dT%H:%M:%S')
        return post
        
    @staticmethod
    def from_dbd(row):
        post = Post()
        post.title = row['Heading']
        post.body = row['Body']
        post.created_date = row['DateCreated']
        return post
    
def dump_posts(posts):
    for post in posts:
        print(post)
        print('----------------------')

def rss_loader(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    return [Post.from_rss(x) for x in root.findall('channel/item')]

def blogml_loader(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    return [Post.from_blogml(x) for x in root.findall('{http://www.blogml.com/2006/09/BlogML}posts/{http://www.blogml.com/2006/09/BlogML}post')]
    
def dbd_loader(connection_string):
    db = create_engine(connection_string)
    
    posts = Table('Post', MetaData(bind=db),
        Column('PostId', Integer, primary_key=True),
        Column('UserId', Integer),
        Column('Active', Boolean),
        Column('Heading', String()),
        Column('Body', String()),
        Column('DateCreated', DateTime),
        Column('DateUpdated', DateTime),
        Column('DateLocked', DateTime))
    
    return [Post.from_dbd(x) for x in posts.select().execute()]

if __name__ == '__main__':
    posts1 = rss_loader('rss.xml')
    #dump_posts(posts1)
    posts2 = blogml_loader('BlogML20Sample.xml')
    dump_posts(posts2)
