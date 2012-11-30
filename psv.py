import sys
import os
import json
import jinja2
from sqlalchemy import *

def load_config(path):
    config_file = open(path)
    config = json.loads(config_file.read())
    config_file.close()
    return config
    
def get_data(config):
    db = create_engine(config['connection_string'])
    
    posts = Table('Post', MetaData(bind=db),
        Column('PostId', Integer, primary_key=True),
        Column('UserId', Integer),
        Column('Active', Boolean),
        Column('Heading', String()),
        Column('Body', String()),
        Column('DateCreated', DateTime),
        Column('DateUpdated', DateTime),
        Column('DateLocked', DateTime))
    
    query = posts.select()
    result = query.execute()
    
    return result
    
def slugify(name):
    name = name.replace('?', '')
    name = name.replace('!', '')
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace('\\', '')
    name = name.replace('/', '')
    return name.replace(' ', '-')
    
def format_datetime(value):
    return value.strftime('%d/%m/%Y %H:%M')
    
def go(config): 
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.', encoding='utf-8'))
    env.filters['datetime'] = format_datetime
    template = env.get_template(config['template'])
    if not os.path.exists(config['out_path']):
        os.makedirs(config['out_path'])
    data = get_data(config)
    for row in data:
        markup = template.render(data=row)
        filename = '{0}/{1}.html'.format(config['out_path'], slugify(row['Heading']))
        f = open(filename, 'w')
        f.write(markup)
        f.close()

if __name__ == '__main__':
    config = load_config(sys.argv[1])
    go(config)
    