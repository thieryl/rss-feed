# -*- coding: utf-8 -*-
"""Simple RSS to HTML converter."""

__version__ = "0.0.1"
__author__ = "Ricky L Wilson"

from unicodedata import normalize

from bs4 import BeautifulSoup
from feedparser import parse as parse_feed

TEMPLATE = u"""
<h2 class='title'>{title}</h2>
<a class='link' href='{link}'>{title}</a>
<span class='description'>{summary}</span>
"""


def flatten_unicode_keys(entry_properties):
    """Ensures passing unicode keywords to **kwargs."""
    for key in entry_properties:
        if isinstance(key, unicode):
            value = entry_properties[key]
            del entry_properties[key]
            entry_properties[normalize('NFKD', key).encode('ascii',
                                                           'ignore')] = value


def entry_to_html(**kwargs):
    """Formats feedparser entry."""
    flatten_unicode_keys(kwargs)
    return TEMPLATE.format(**kwargs).encode('utf-8')


def convert_feed(url):
    """Main loop."""
    html_fragments = [
        entry_to_html(**entry) for entry in parse_feed(url).entries
    ]
    return BeautifulSoup("\n".join(html_fragments), 'lxml').prettify()


def save_file(url, filename):
    """Saves data to disc."""
    with open(filename, 'w') as file_object:
        file_object.write(convert_feed(url).encode('utf-8'))


if __name__ == '__main__':
    save_file('http://stackoverflow.com/feeds', 'index.html')
