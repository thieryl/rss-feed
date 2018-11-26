from feedparser import parse as parse_feed

from mako.template import Template


def convert_feed(url, filename):
    """Convert feed to an HTML."""
    with open(filename, 'w') as file_object:
        feeds = parse_feed(url).entries
        html_content = Template(
            filename='template.html',
            output_encoding='utf-8').render(feeds=feeds)
        file_object.write(html_content)


if __name__ == '__main__':
    convert_feed('http://stackoverflow.com/feeds', 'index.html')
