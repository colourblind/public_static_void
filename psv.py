import sys
import os
import json
import jinja2
import feed_parser
import modifiers

def load_config(path):
    config_file = open(path)
    config = json.loads(config_file.read())
    config_file.close()
    return config
    
def slugify(name):
    name = name.replace('?', '')
    name = name.replace('!', '')
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace('\\', '')
    name = name.replace('/', '')
    name = name.replace(':', '')
    name = name.replace('\'', '')
    name = name.replace('"', '')
    return name.replace(' ', '-')
    
def format_datetime(value):
    return value.strftime('%d/%m/%Y %H:%M')
    
def format_slug(value):
    return slugify(value)
    
def go(config): 
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.', encoding='utf-8'))
    env.filters['datetime'] = format_datetime
    env.filters['slug'] = format_slug
    template = env.get_template(config['template'])
    index_template = env.get_template(config['index_template']);
    if not os.path.exists(config['out_path']):
        os.makedirs(config['out_path'])
    # TODO: pick loaders dynamically
    data = feed_parser.rss_loader(config['connection_string'])
    for row in data:
        row.body = modifiers.tweak(row.body)
        markup = template.render(data=row)
        filename = '{0}/{1}.html'.format(config['out_path'], slugify(row.title))
        print('<add from="/post/{0}.aspx" to="/{1}.html" />'.format(slugify(row.title).lower(), slugify(row.title)))
        f = open(filename, 'w')
        f.write(markup)
        f.close()
        
    # Create homepage
    f = open('{0}/index.html'.format(config['out_path']), 'w')
    f.write(index_template.render(data=data))
    f.close()
    
if __name__ == '__main__':
    config = load_config(sys.argv[1])
    go(config)
    